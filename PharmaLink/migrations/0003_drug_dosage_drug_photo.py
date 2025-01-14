# Generated by Django 4.2.3 on 2023-10-12 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PharmaLink', '0002_drug_remove_inventory_drug_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='dosage',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='drug',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='drug_photos'),
        ),
    ]
