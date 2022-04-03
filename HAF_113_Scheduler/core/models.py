from email.policy import default
from django.db import models
import os
from django.dispatch import receiver


class UploadedFile(models.Model):
    filename = models.CharField(max_length=200,null=True)
    file = models.FileField()

class Airman(models.Model):
    asma = models.BigIntegerField(primary_key=True)
    firstname = models.CharField(max_length=200,default="",blank=True,null=True)
    lastname = models.CharField(max_length=200,default="",blank=True,null=True)
    rank = models.CharField(max_length=200,default="",blank=True,null=True)
    eidikotita = models.CharField(max_length=200,default="",blank=True,null=True)
    idiotita = models.CharField(max_length=200,default="",blank=True,null=True)
    availability = models.CharField(max_length=200,default="",blank=True,null=True)
    topothetisi = models.CharField(max_length=200,default="",blank=True,null=True)
    katigoria_ptitikou = models.CharField(max_length=200,default="",blank=True,null=True)
    monada_ekdosis_ptitikou = models.CharField(max_length=200,default="",blank=True,null=True)
    geniko_synolo_oron = models.FloatField(blank=True,null=True,default=0)
    def __str__(self):
        return (str(self.asma) + " - " + self.lastname + " " + self.firstname)

class FlightHours(models.Model):
    airman = models.ForeignKey(Airman,on_delete=models.CASCADE)
    plane = models.CharField(max_length=200,default="",blank=True,null=True)
    capthours = models.FloatField(blank=True,null=True,default=0)
    cocapthours = models.FloatField(blank=True,null=True,default=0)
    ifrhours = models.FloatField(blank=True,null=True,default=0)
    nighthours = models.FloatField(blank=True,null=True,default=0)
    nauthours = models.FloatField(blank=True,null=True,default=0)
    crewhours = models.FloatField(blank=True,null=True,default=0)
    category = models.CharField(max_length=200,default="",blank=True,null=True)
    unit = models.CharField(max_length=200,default="",blank=True,null=True)
    month = models.CharField(max_length=200,default="",blank=True,null=True)
    year = models.CharField(max_length=200,default="",blank=True,null=True)
    def __str__(self):
        return (str(self.airman.asma) + " - " + self.airman.lastname + " - "+ self.month + " " + self.year)

class TrainHours(models.Model):
    airman = models.ForeignKey(Airman,on_delete=models.CASCADE)
    plane = models.CharField(max_length=200,default="",blank=True,null=True)
    hours = models.FloatField(blank=True,null=True,default=0)
    month = models.CharField(max_length=200,default="",blank=True,null=True)
    year = models.CharField(max_length=200,default="",blank=True,null=True)
    def __str__(self):
        return (str(self.airman.asma) + " - " + self.airman.lastname + " - "+ self.month + " " + self.year)


@receiver(models.signals.post_delete, sender=UploadedFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)