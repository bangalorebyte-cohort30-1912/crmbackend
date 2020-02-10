from rest_framework import serializers
from leads.models import Lead, LeadStage
from salespersons.models import SalesPersonUser
from salespersons.serializers import SalesPersonUserSerializer
from mailengine.models import EventLog
from leads.utils import assign_salesperson
from django.utils import timezone
from django.core.mail import send_mail
from mailengine.tasks import followup


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'
        # read_only_fields = ['assigned_to', 'status']
    
    def create(self, validated_data):
        lead_object = Lead(status=LeadStage.objects.get(pk=1),**validated_data)
        lead_object.save()
        salesperson = assign_salesperson()
        manager = SalesPersonUser.objects.get(pk=1) if salesperson.manager == None else salesperson.manager
        lead_object.assigned_to.set([salesperson])
        lead_object.save()
        eventlog_obj = EventLog(event_lead=lead_object, event_type="New Lead", salesperson=salesperson, manager=manager)
        eventlog_obj.save()
        send_mail('New Lead', f'New Lead assigned to { salesperson.email }', 'tempbytedeveloper@gmail.com', [salesperson.email, manager.email], fail_silently=False,)
        followup.delay(event_id=eventlog_obj.id, type='regular')
        return lead_object


class LeadStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadStage
        fields = '__all__'


class LeadGetSerializer(serializers.ModelSerializer):
    assigned_to = SalesPersonUserSerializer(many=True)

    class Meta:
        abstract = True
        model = Lead
        fields = '__all__'
        depth = 1



    
