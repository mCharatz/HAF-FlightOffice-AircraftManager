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


def index(request):
    return render(request,'core/index.html')

def upload(request):
    return render(request,'core/eisagogi_dedomenon/upload_file.html')

def upload_file_success(request):
    return render(request,'core/eisagogi_dedomenon/upload_file_success.html')

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
    
        return save_data(data,month,year)
    else:
        return redirect("/")
    
def flight_hours(request):
    table_data = FlightHours.objects.all().order_by('airman__lastname')
    context = {'table_data':table_data}
    return render(request,'core/flight_hours_page.html',context)

def prosopiko_eksaminou(request):
    eksaminoi = Airman.objects.filter(flighthours__category="6ΜΗΝΟ").order_by('lastname')
    context = {'table_data':eksaminoi}
    return render(request,'core/vevaioseis/six_months.html',context)

def prosopiko_dekaotaminou(request):
    dekaoktaminoi = Airman.objects.filter(flighthours__category="18ΜΗΝΟ").order_by('lastname')
    context = {'table_data':dekaoktaminoi}
    return render(request,'core/vevaioseis/eighteen_months.html',context)

def trainers(request):
    trainers = AirmanTrainer.objects.all()
    context = {'table_data':trainers}
    return render(request,'core/vevaioseis/trainers.html',context)

def pilots(request):
    pilots = Airman.objects.filter(eidikotita="Ι")
    context = {'table_data':pilots}
    return render(request,'core/vevaioseis/ypa.html',context)

def train_hours(request):
    context = {}
    table_data = TrainHours.objects.all().order_by('airman__lastname')
    context = {'table_data':table_data}
    return render(request,'core/train_hours_page.html',context)

def profile(request,asma):
    try:
        airman = Airman.objects.get(asma=asma)
        flight_hours = FlightHours.objects.filter(airman=airman)
        train_hours = TrainHours.objects.filter(airman=airman)
    except:
        return redirect('/')
    context = {
        'pilot':airman,
        'flight_hours':flight_hours,
        'train_hours':train_hours
    }
    return render(request,'core/airman_profile.html',context)