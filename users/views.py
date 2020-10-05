from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import Http404
from django.db.models import Sum, Count
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from django.contrib import messages

from .forms import NewUserForm, UpgradeUserForm
from .models import KedataUsers, UsageKeywordListening, UsageKeywordComparison, UsageKeywordMultikey, LastUpdateTime

from . import view_funcs
from datetime import datetime

from . import tasks

secret_key = settings.RABBIT_SECRET_KEY


# Create your views here.
class HomeView(ListView):
    model = KedataUsers
    context_object_name = 'user_data'
    template_name = 'users/base_user.html'
    ordering = ['-last_login']

    def get_context_data(self, **kwargs):
        try:
            kwargs['sub_labels'], kwargs['sub_datas'] = view_funcs.get_user_report_data('subscription')
            kwargs['pro_labels'], kwargs['pro_datas'] = view_funcs.get_user_report_data('project_name')
            kwargs['last_updated_time'] = get_object_or_404(LastUpdateTime, id=1).last_updated_user
        except:
            pass
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):                
        tasks.update_kedata_users()
        messages.add_message(self.request, messages.SUCCESS, 'Updating Users In Background')        
        return redirect('users:home')

class NewUserView(FormView):    
    template_name = 'users/new_user.html'
    form_class = NewUserForm
    success_url = reverse_lazy('users:home')

    def form_valid(self, form):
        temp_dict = {'name': '-', 'company': '-', 'phone': '-'}
        json_dict = form.cleaned_data
        json_dict["secret_key"] = secret_key
        json_dict.update(temp_dict)
        json_dict["password"] = view_funcs.random_password_generator(12)        
        # tasks.new_user_pika(json_dict) #HUEY NEW USER
        response = view_funcs.call_pika_exchange(
            'endgraf.dashboard.register_account.retrieve',
            'kedata.dashboard.register_account.register',
            json_dict
            )        
        # print(response)
        if response:
            if not 'content' in response:
                messages.add_message(self.request, messages.WARNING, 'Error updating user')
                return redirect('users:new_user')
        messages.add_message(self.request, messages.SUCCESS, 'Created new user')        
        return super().form_valid(form)

def user_upgrade_view(request, email=None):    
    if request.POST:
        form = UpgradeUserForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data            
            status['secret_key'] = secret_key     
            # tasks.upgrade_user_pika(status)   #HUEY TASK    
            response = view_funcs.call_pika_exchange(
                'endgraf.dashboard.upgrade_status.retrieve',
                'kedata.dashboard.upgrade_status.retrieve',
                status
                )
            print(response)
            if not response:
                messages.add_message(request, messages.ERROR, 'No Response')
                return redirect('users:home')
            if response['content']['message'] != 'success':
                messages.add_message(request, messages.ERROR, 'Error Updating User')
                return redirect('users:upgrade_user_no_email')
            update_id = response['content']['data']['user_id']
            KedataUsers.objects.filter(user_id=update_id).update(subscription=status['add_status'])
            messages.add_message(request, messages.SUCCESS, 'Success Updating User')
            return redirect('users:home')            
    else:
        form = UpgradeUserForm(initial={'email': email})
        kedata_users = KedataUsers.objects.all()
    return render(request, 'users/upgrade_user.html', {'form': form, 'user_data': kedata_users})

