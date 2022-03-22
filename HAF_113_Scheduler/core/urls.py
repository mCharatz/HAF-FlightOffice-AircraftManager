from django.urls import path
from . import views

urlpatterns = [
    path('',views.upload,name="upload_file"),
    path('upload/',views.proccess_uploaded_data,name="proccess_data"),
    path('save/',views.save_uploaded_data,name="save_uploaded_data"),
]
