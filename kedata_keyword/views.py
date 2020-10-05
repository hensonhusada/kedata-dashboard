from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages

from django.views.generic import TemplateView, ListView

from users.models import UsageKeywordListening, KedataUsers, UsageKeywordComparison, UsageKeywordMultikey, LastUpdateTime

from .tasks import usage_keyword_update, send_email
from .models import LogKeywordCount
from . import view_funcs
from .forms import KeywordStateForm, CreateIssueForm
from datetime import datetime
import json
from django.core.mail import EmailMultiAlternatives, send_mail
secret_key = settings.RABBIT_SECRET_KEY

RESPONSE_EXCHANGE_NAME = 'endgraf.responses.direct'

# Create your views here.
def homeview(request, year=datetime.now().year):
    if request.POST:
        usage_keyword_update()
        messages.add_message(request, messages.SUCCESS, 'Updating Keywords In Background')
        
    keyword_data_listening = []
    keyword_data_comparison = []
    keyword_data_multi= []
    if request.GET.get('year'):
        year = request.GET['keyChart_date']
    for i in range(1,13):
        keyword_data_listening.append(UsageKeywordListening.objects.filter(timestamps__month=str(i), timestamps__year=year).count())
        keyword_data_comparison.append(UsageKeywordComparison.objects.filter(timestamps__month=str(i), timestamps__year=year).count())
        keyword_data_multi.append(UsageKeywordMultikey.objects.filter(timestamps__month=str(i), timestamps__year=year).count())

    keyword_labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    try:
        last_update_time = LastUpdateTime.objects.get(id=1).last_updated_keyword
    except:
        last_update_time = ''

    try:
        keyword_data = LogKeywordCount.objects.get(id=1)     
        json_data_media = json.loads(keyword_data.json_data_media)
        json_data_name = json.loads(keyword_data.json_data_name)
    except Exception as e:
        print('Error', e)
        json_data_media = ''
        json_data_name = ''

    return render(request, 'kedata_keyword/base_keyword.html',
        {'last_update': last_update_time,
        'json_data_media': json_data_media,
        'json_data_name': json_data_name,
        'lis_datas': keyword_data_listening,
        'com_datas': keyword_data_comparison,
        'mul_datas': keyword_data_multi,
        'keyword_labels': keyword_labels,
        'year': year
        })

# NEED FIX (?)
# Keyword state update views, redirect to list of keywords
def stateview(request, type='listening', key_id=None):
    if request.POST:
        next = request.POST.get('next', '/')
        form = KeywordStateForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data
            status['id'] = status.pop('keyword_id')
            status['secret_key'] = secret_key
            response = view_funcs.call_pika_exchange(
                'endgraf.dashboard.keyword_state.retrieve',
                'kedata.dashboard.keyword_state.retrieve',
                status
                )
            key_id = status['id']
            type = status['fields']
            if 'error' in response:
                messages.add_message(request, messages.ERROR, 'Error: No such key')
                return redirect('keyword:state')
            messages.add_message(request, messages.SUCCESS, 'Success updating keyword')
            # print(response)
            if type=='listening':
                UsageKeywordListening.objects.filter(keyword_id=key_id).update(state=status['status'])
                con = UsageKeywordListening.objects.get(keyword_id=key_id)
                return redirect('keyword:keyword', con.user_id.user_id)
            elif type=='comparison':
                UsageKeywordComparison.objects.filter(keyword_id=key_id).update(state=status['status'])
                con = UsageKeywordComparison.objects.get(keyword_id=key_id)
                return redirect('keyword:keyword', con.user_id.user_id)
            else:
                UsageKeywordMultikey.objects.filter(keyword_id=key_id).update(state=status['status'])
                con = UsageKeywordMultikey.objects.get(keyword_id=key_id)
                return redirect('keyword:keyword', con.user_id.user_id)

    else:
        form = KeywordStateForm(initial={'fields': type, 'keyword_id': key_id})
    return render(request, 'kedata_keyword/state_keyword.html', {'form': form})

#View keywords per user
def users_keyword_view(request, user_id):
    try:
        last_updated_time = LastUpdateTime.objects.get(id=1).last_updated_keyword
    except:
        last_updated_time = ''
    kedata_user = get_object_or_404(KedataUsers, user_id=user_id)
    user_listening = UsageKeywordListening.objects.filter(user_id=kedata_user.user_id)
    user_comparison = UsageKeywordComparison.objects.filter(user_id=kedata_user.user_id)
    user_multikey = UsageKeywordMultikey.objects.filter(user_id=kedata_user.user_id)

    return render(request, 'kedata_keyword/user_keyword.html', {'user_data': kedata_user, 'user_listening': user_listening, 'user_comparison': user_comparison, 'user_multikey': user_multikey, 'last_update': last_updated_time})

def create_issue_view(request, type='listening', key_id=None):
    if request.POST:
        form = CreateIssueForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            if data['fields'] == 'listening':
                try:
                    temp = UsageKeywordListening.objects.get(keyword_id=data['keyword_id'])
                    message = json.dumps({'id': temp.keyword_id, 'text':temp.text, 'media': temp.media, 'state': temp.state, 'timestamp': datetime.timestamp(datetime.now())})
                except:
                    messages.add_message(request, messages.ERROR, 'Key does not exist')
                    return redirect('keyword:create_issue')
            elif data['fields'] == 'comparison':
                try:
                    temp = UsageKeywordComparison.objects.get(keyword_id=data['keyword_id'])
                    message = json.dumps({'id': temp.keyword_id, 'name':temp.name, 'media': temp.media, 'state': temp.state, 'timestamp': datetime.timestamp(datetime.now())})
                except:
                    messages.add_message(request, messages.ERROR, 'Key does not exist')
                    return redirect('keyword:create_issue')
            else:
                try:
                    temp = UsageKeywordMultikey.objects.get(keyword_id=data['keyword_id'])
                    message = json.dumps({'id': temp.keyword_id, 'name': temp.name, 'media': temp.media, 'state': temp.state, 'timestamp': datetime.timestamp(datetime.now())})
                except:
                    messages.add_message(request, messages.ERROR, 'Key does not exist')
                    return redirect('keyword:create_issue')
            
            send_email(message)
            messages.add_message(request, messages.SUCCESS, 'Sending email in background')
    else:
        form = CreateIssueForm(initial={'fields': type, 'keyword_id': key_id})
    return render(request, 'kedata_keyword/create_issue.html', {'form': form})

def awesom_view():
    subject = 'Hello, its me'
    text_content = "I was wondering if after all these years"
    sender = "hensonhusada@gmail.com"
    receipient = "henzonlol@gmail.com"
    msg = EmailMultiAlternatives(subject, text_content, sender, [receipient])
    response = msg.send()
    return response