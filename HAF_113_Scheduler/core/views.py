import imp
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .process_file_data import *
from .models import *
# Create your views here.

def upload(request):
    return render(request,'core/upload_file.html')

def proccess_uploaded_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                uploaded = request.FILES.getlist('files')
                uploaded_file = uploaded[0]
                
                file_db = UploadedFile.objects.create(
                    filename = uploaded_file.name,
                    file = uploaded_file
                )
                if file_db == None:
                    return redirect("/")

                table_data,file_type = create_tsv_files(file_db)
                file_db.delete()
            except:
                return redirect("/")
            
            context = {'table_data': table_data,'file_type':file_type}
            return render(request,'core/pilot_hours.html',context)
    return redirect("/")

