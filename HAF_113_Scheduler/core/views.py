from calendar import month
import imp
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .process_file_data import *
from .save_file_data import save_data
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
    months = {
        1: 'ΙΑΝΟΥΑΡΙΟΣ',
        2: 'ΦΕΒΡΟΥΑΡΙΟΣ',
        3: 'ΜΑΡΤΙΟΣ',
        4: 'ΑΠΡΙΛΙΟΣ',
        5: 'ΜΑΙΟΣ',
        6: 'ΙΟΥΝΙΟΣ',
        7: 'ΙΟΥΛΙΟΣ',
        8: 'ΑΥΓΟΥΣΤΟΣ',
        9: 'ΣΕΠΤΕΜΒΡΙΟΣ',
        10: 'ΟΚΤΩΒΡΙΟΣ',
        11: 'ΝΟΕΜΒΡΙΟΣ',
        12: 'ΔΕΚΕΜΒΡΙΟΣ'
    }
    logger = logging.getLogger("mylogger")
    if request.method == "POST":
        data = request.POST.lists()
        data2 = list(copy.copy(data))
        month = None
        year = None
        for item in data2:
            if item[0] == 'month':
                month = item[1][0]
            elif item[0] == 'year':
                year = item[1][0]
        
        logger.info(month)
        logger.info(year)
        save_data(data,month,year)
        return HttpResponse("ok")
    else:
        return redirect("/")
    
