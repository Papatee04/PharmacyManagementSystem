# Generated by Django 4.2.3 on 2023-10-18 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PharmaLink', '0010_remove_prescription_prescribe_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
