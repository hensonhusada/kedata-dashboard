from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ScheduleForm
from .models import ScheduleList
from datetime import datetime
import uuid

from .tasks import make_schedule, finish_schedule
from django.views.generic import ListView

# Create your views here.
def schedule_view(request):
    if request.POST:
        new_id = uuid.uuid4()
        form = ScheduleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            make_schedule(data['media'], new_id)
            messages.add_message(request, messages.SUCCESS, 'Creating schedule in background!')
            finish_schedule.schedule(kwargs={'id': new_id}, delay=10)
            return redirect('schedule:schedule')

    else:
        form = ScheduleForm()
    return render(request, 'schedule/schedule.html', {'form': form})

class ScheduleListView(ListView):
    model = ScheduleList
    context_object_name = 'schedule_items'
    template_name = 'schedule/schedule_list.html'
    