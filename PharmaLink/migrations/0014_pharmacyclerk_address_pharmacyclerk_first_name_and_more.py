# Generated by Django 4.2.3 on 2023-10-23 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PharmaLink', '0013_delete_patientfeedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='pharmacyclerk',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='pharmacyclerk',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pharmacyclerk',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
