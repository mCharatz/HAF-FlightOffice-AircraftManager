from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('add/uploadFile/',views.upload,name="upload_file"),
    path('add/uploadFile/success',views.upload_file_success,name="upload_file_success"),
    path('add/flightHour/',views.add_flight_hour,name="add_flight_hour"),
    path('add/trainHour/',views.add_train_hour,name="add_train_hour"),
    path('add/flightHour/success',views.add_flight_hour_suceess,name="add_flight_hour_suceess"),
    path('add/flightHour/exist',views.add_flight_hour_exist,name="add_flight_hour_exist"),
    path('add/trainHour/success',views.add_train_hour_suceess,name="add_train_hour_suceess"),
    path('add/trainHour/exist',views.add_train_hour_exist,name="add_train_hour_exist"),
    path('upload/',views.proccess_uploaded_data,name="proccess_data"),
    path('save/',views.save_uploaded_data,name="save_uploaded_data"),
    path('vevaioseis/',views.vevaioseis,name="vevaioseis"),
    path('staff/6-months/',views.prosopiko_eksaminou,name="prosopiko_eksaminou"),
    path('staff/18-months/',views.prosopiko_dekaotaminou,name="prosopiko_dekaotaminou"),
    path('staff/trainers/',views.trainers,name="trainers"),
    path('staff/pilots/',views.pilots,name="pilots"),
    path('hours/flight-hours/',views.flight_hours,name="flight_hours"),
    path('hours/train-hours/',views.train_hours,name="train_hours"),
    path('profile/<slug:asma>/',views.profile,name="profile"),
    path('add/flightHour/find',views.findasma,name="findasma"),
    path('search/',views.search,name="search"),
    path('change/',views.changetabledata,name="changeTableData")
    
]
