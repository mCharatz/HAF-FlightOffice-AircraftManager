from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('add/uploadFile/',views.upload,name="upload_file"),
    path('add/uploadFile/success',views.upload_file_success,name="upload_file_success"),
    path('upload/',views.proccess_uploaded_data,name="proccess_data"),
    path('save/',views.save_uploaded_data,name="save_uploaded_data"),
    path('staff/6-months/',views.prosopiko_eksaminou,name="prosopiko_eksaminou"),
    path('staff/18-months/',views.prosopiko_dekaotaminou,name="prosopiko_dekaotaminou"),
    path('staff/trainers/',views.trainers,name="trainers"),
    path('staff/pilots/',views.pilots,name="pilots"),
    path('hours/flight-hours/',views.flight_hours,name="flight_hours"),
    path('hours/train-hours/',views.train_hours,name="train_hours"),
    path('profile/<slug:asma>/',views.profile,name="profile")
]
