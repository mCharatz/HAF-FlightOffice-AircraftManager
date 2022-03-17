from django.db import models
import os
from django.dispatch import receiver
# Create your models here.

class UploadedFile(models.Model):
    filename = models.CharField(max_length=200,null=True)
    file = models.FileField()

@receiver(models.signals.post_delete, sender=UploadedFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)