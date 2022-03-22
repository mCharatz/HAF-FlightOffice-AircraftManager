import imp
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .process_file_data import *
from .save_file_data import *
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

def save_uploaded_data(request):
    #TODO FIX THIS IN ORDER TO SAVE DATA
    logger = logging.getLogger("mylogger")
    if request.method == "POST":
        data = request.POST.lists()
        for airman in data:
            if len(airman[1]) != 16:
                continue
            try:
                airman_item = Airman.objects.get(asma=airman[1][0])
            except:
                airman_item = Airman.objects.create(
                    asma = airman[1][0],
                    firstname = airman[1][1],
                    lastname = airman[1][2],
                    rank = airman[1][2],
                    eidikotita = airman[1][4]
                )
            FlightHours.objects.create(
                airman = airman_item,
                plane = airman[1][5]
            )
        return HttpResponse("ok")
    else:
        return redirect("/")
    
