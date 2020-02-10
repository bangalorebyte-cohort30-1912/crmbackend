from django.db import models
from salespersons.models import SalesPersonUser
from leads.models import Lead, LeadStage

EVENT_TRIGGERS = (
    ('New Lead', 'New Lead'),
    ('Lead Status Change', 'Lead Status Change'),
    ('Lead Reassigned', 'Lead Reassigned'),
    ('Regular Follow up', 'Regular Follow up'),
    ('Escalation', 'Escalation'),
)


class EventLog(models.Model):
    event_lead = models.ForeignKey(Lead, on_delete=models.DO_NOTHING, related_name='event_lead')
    event_created_on = models.DateTimeField("Created on", auto_now_add=True)
    event_type = models.CharField("Type of Event", max_length=255, choices=EVENT_TRIGGERS)
    salesperson = models.ForeignKey(SalesPersonUser, on_delete=models.DO_NOTHING, related_name='lead_assigned_salesperson')
    manager = models.ForeignKey(SalesPersonUser, on_delete=models.DO_NOTHING, related_name='lead_assigned_manager', null=True)
    # due_time = models.DateTimeField()

    def __str__(self):
        return f"{ self.event_lead } { self.event_type } for {self.salesperson }"

