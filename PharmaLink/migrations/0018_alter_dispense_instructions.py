# Generated by Django 4.2.3 on 2023-10-26 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PharmaLink', '0017_remove_dispense_drug_id_dispense_drug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispense',
            name='instructions',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
