# Generated by Django 3.0.2 on 2020-01-31 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_auto_20200131_1810'),
        ('mailengine', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventlog',
            name='due_time',
        ),
        migrations.RemoveField(
            model_name='eventlog',
            name='lead_event',
        ),
        migrations.AddField(
            model_name='eventlog',
            name='event_lead',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='event_lead', to='leads.Lead'),
            preserve_default=False,
        ),
    ]