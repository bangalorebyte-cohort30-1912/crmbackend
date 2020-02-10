from django.shortcuts import render
from mailengine.tasks import add, followup
from mailengine.models import EventLog
from django.http import HttpResponse

# Create your views here.

def celerytest(request):
    print("something should run here..")
    followup.delay(event_id=1, type='regular')
    print("testing")
    return HttpResponse("Executed")
