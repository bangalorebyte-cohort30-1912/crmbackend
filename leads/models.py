from django.db import models
from salespersons.models import SalesPersonUser

LEAD_SOURCE = (
    ('call', 'Call'),
    ('website', 'Website'),
    ('email', 'Email'),
    ('existing customer', 'Existing Customer'),
    ('partner', 'Partner'),
    ('public relations', 'Public Relations'),
    ('compaign', 'Campaign'),
    ('other', 'Other'),
)

LEAD_STATUS = (
    ('Not Updated', 'Not Updated'),
    ('BD Call', 'BD Call'),
    ('Meeting', 'Meeting'),
    ('Proposal', 'Proposal')
)

ROLE = (
    ('Business Owner/Leader', 'Business Owner/Leader'),
    ('Media', 'Media'),
    ('Director HR/Talent Acquisition', 'Director HR/Talent Acquisition'),
    ('Job Seeker', 'Job Seeker'),
    ('Recruiter/Sourcer', 'Recruiter/Sourcer')
)

ENQUIRY_TYPE = (
    ('Sales Enquiry', 'Sales Enquiry'),
    ('Job Seeker', 'Job Seeker'),
    ('Media','Media')
)

class LeadStage(models.Model):
    name = models.CharField("Name", max_length=255)
    followup_wait = models.BigIntegerField(default=2)
    escalation_wait = models.BigIntegerField(default=2)

    def __str__(self):
        return f"Lead Stage {self.name} with follow up delay {self.followup_wait} and escalation {self.escalation_wait} setup."

class Lead(models.Model):
    first_name = models.CharField("First name", max_length=255)
    last_name = models.CharField("Last name", max_length=255)
    type_of_enquiry = models.CharField("Type of Enquiry", max_length=255, choices=ENQUIRY_TYPE, default='Sales Enquiry', null=True)
    company = models.CharField("Company", max_length=255, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField("Role", max_length=60, choices=ROLE, default='Business Owner/Leader')
    message = models.TextField(null=True, blank=True)
    positions_to_fill = models.BigIntegerField(null=True)
    service_requirements = models.CharField(
        max_length=100000, null=True, blank=True)
    loc_of_hire = models.CharField(max_length=100000, null=True, blank=True)
    industry = models.CharField(max_length=100000, null=True, blank=True)
    comp_emp_strength = models.BigIntegerField(null=True)
    form_submission_time = models.CharField(
        max_length=100000, null=True, blank=True)
    form_type = models.CharField(max_length=100000, null=True, blank=True)
    status = models.ForeignKey(LeadStage, on_delete=models.DO_NOTHING,
                               default=1, related_name='lead_leadstage')
    source = models.CharField("Source of Lead", max_length=255,
                              blank=True, null=True, choices=LEAD_SOURCE, default="website")
    assigned_to = models.ManyToManyField(
        SalesPersonUser, related_name='lead_assigned_salespersonusers', blank=True)
    createdOn = models.DateTimeField("Created on", auto_now_add=True)

    def __str__(self):
        return f"{self.email} with {self.first_name} {self.last_name}"






