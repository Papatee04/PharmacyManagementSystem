# Generated by Django 4.2.3 on 2023-10-12 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PharmaLink', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=100, null=True)),
                ('strength', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='drug_color',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='drug_description',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='drug_imprint',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='drug_name',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='drug_pic',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='drug_shape',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='drug_strength',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='manufacture',
        ),
        migrations.AddField(
            model_name='dispense',
            name='prescription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='PharmaLink.prescription'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='drug',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='PharmaLink.drug'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='drug',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='PharmaLink.drug'),
        ),
    ]