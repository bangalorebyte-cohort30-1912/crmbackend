from __future__ import absolute_import, unicode_literals

from celery import shared_task
import time
from mailengine.models import EventLog
from django.core.mail import send_mail
from crmtest.settings import EMAIL_HOST_USER
from leads.models import Lead, LeadStage
from salespersons.models import SalesPersonUser


@shared_task
def add(x, y):
    time.sleep(10)
    return x + y


@shared_task
def followup(event_id=1, type='regular'):
    print(f"inside followup with event_id : {event_id}")
    eventlog_obj = EventLog.objects.get(pk=event_id)
    lead = eventlog_obj.event_lead
    wait = lead.status.followup_wait if type=='regular' else lead.status.escalation_wait
    time.sleep(wait)
    latest_eventlog_obj = EventLog.objects.filter(event_lead=lead).last()
    if eventlog_obj.id == latest_eventlog_obj.id:
        print(f"So no new eventlog_object for {wait} seconds and sending followup Mail")
        lead = eventlog_obj.event_lead
        salesperson = lead.assigned_to.all()[0]
        manager = SalesPersonUser.objects.get(pk=1) if lead.assigned_to.all()[0].manager == None else lead.assigned_to.all()[0].manager
        subject = f"{type} follow up Mail on Lead :{eventlog_obj.event_lead.id} due to inactivity"
        message = f"Lead : {eventlog_obj.event_lead.id} has been inactive for {wait} seconds."
        recepient = [salesperson.email] if type=='regular' else [manager.email, salesperson.email]
        print(f"{type} Mail send to {recepient}..")
        send_mail(subject, message, EMAIL_HOST_USER, recepient, fail_silently=False)
        print(f"{type} follow up Mail triggered..")
        if type=='regular':
            print("Escalation Triggered..")
            followup.delay(event_id=event_id, type="ESCALATION")
        return print(f"Exiting cycle for {event_id}..")
    else:
        print(f"Lead : {lead.id} has had some action hence exiting..")
    return
