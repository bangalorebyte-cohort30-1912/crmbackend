from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from leads.models import Lead, LeadStage

from salespersons.models import SalesPersonUser
from leads.serializers import LeadSerializer, LeadGetSerializer
from django.http import HttpResponse

from mailengine.models import EventLog
from mailengine.tasks import followup

from django.core.mail import send_mail
import json

# Create your views here.


class LeadModelView(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LeadGetSerializer
        else:
            return self.serializer_class

    def partial_update(self, request, pk):
        data_dict = json.loads(f"{request.body.decode()}")
        if 'status' in data_dict.keys():
            lead = Lead.objects.get(pk=pk)
            lead.status = LeadStage.objects.get(pk=data_dict['status'])
            lead.save()
            manager = SalesPersonUser.objects.get(pk=1) if lead.assigned_to.all() == None else lead.assigned_to.all()[0].manager
            salesperson = lead.assigned_to.all()[0]
            eventlog_object = EventLog(event_lead=lead, event_type="Lead Status Change", salesperson = salesperson, manager=manager)
            eventlog_object.save()
            send_mail('Lead Status Changed', f'Lead Status for { lead.id }', 'tempbytedeveloper@gmail.com', [salesperson.email, manager.email], fail_silently=False,)
            followup.delay(event_id=eventlog_object.id, type='regular')
        if 'assigned_to' in data_dict.keys():
            lead = Lead.objects.get(pk=pk)
            lead.assigned_to.set([SalesPersonUser.objects.get(pk=data_dict['assigned_to'][0])])
            lead.save()
            manager = SalesPersonUser.objects.get(pk=1) if lead.assigned_to.all() == None else lead.assigned_to.all()[0].manager
            salesperson = lead.assigned_to.all()[0]
            eventlog_object = EventLog(event_lead=lead, event_type="Lead Reassigned", salesperson=salesperson, manager=manager)
            eventlog_object.save()
            send_mail('Lead assigned to you ', f'New Lead is assigned with {lead.id}', 'tempbytedeveloper@gmail.com', [salesperson.email, manager.email], fail_silently=False,)
            followup.delay(event_id=eventlog_object.id, type='regular')
        data = LeadSerializer(Lead.objects.get(pk=pk)).data
        return Response(data=data)
