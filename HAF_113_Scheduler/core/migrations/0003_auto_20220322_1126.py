# Generated by Django 3.2.12 on 2022-03-22 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_airman_flighthours_trainhours'),
    ]

    operations = [
        migrations.RenameField(
            model_name='airman',
            old_name='speciality',
            new_name='eidikotika',
        ),
        migrations.AddField(
            model_name='airman',
            name='availability',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='airman',
            name='idiotita',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='airman',
            name='monada_ekdosis_ptitikou',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
