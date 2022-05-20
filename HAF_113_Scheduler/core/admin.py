from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Airman)
admin.site.register(AirmanTrainer)
admin.site.register(FlightHours)
admin.site.register(TrainHours)
