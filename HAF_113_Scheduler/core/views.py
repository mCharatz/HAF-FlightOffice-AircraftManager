from calendar import month
import imp
from unicodedata import category
from warnings import catch_warnings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from .forms import UploadFileForm
from .process_file_data import *
from .save_file_data import save_data
from .save_file_data import *
from .models import *
from .support_func import *
# Create your views here.


def index(request):
    return render(request, 'core/index.html')


def upload(request):
    return render(request, 'core/eisagogi_dedomenon/upload_file.html')


def upload_file_success(request):
    return render(request, 'core/eisagogi_dedomenon/upload_file_success.html')


def proccess_uploaded_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                uploaded = request.FILES.getlist('files')
                uploaded_file = uploaded[0]

                file_db = UploadedFile.objects.create(
                    filename=uploaded_file.name,
                    file=uploaded_file
                )
                if file_db == None:
                    return redirect("/")

                table_data, file_type = create_tsv_files(file_db)
                file_db.delete()
            except:
                return redirect("/")

            context = {'table_data': table_data, 'file_type': file_type}
            return render(request, 'core/pilot_hours.html', context)
    return redirect("/")


def save_uploaded_data(request):
    # TODO FIX THIS IN ORDER TO SAVE DATA
    months = {
        'ΙΑΝΟΥΑΡΙΟΣ': 1,
        'ΦΕΒΡΟΥΑΡΙΟΣ': 2,
        'ΜΑΡΤΙΟΣ': 3,
        'ΑΠΡΙΛΙΟΣ': 4,
        'ΜΑΙΟΣ': 5,
        'ΙΟΥΝΙΟΣ': 6,
        'ΙΟΥΛΙΟΣ': 7,
        'ΑΥΓΟΥΣΤΟΣ': 8,
        'ΣΕΠΤΕΜΒΡΙΟΣ': 9,
        'ΟΚΤΩΒΡΙΟΣ': 10,
        'ΝΟΕΜΒΡΙΟΣ': 11,
        'ΔΕΚΕΜΒΡΙΟΣ': 12
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

        return save_data(data, month, year)
    else:
        return redirect("/")


def flight_hours(request):
    table_data = FlightHours.objects.all().order_by('airman__lastname')
    context = {'table_data': table_data}
    return render(request, 'core/flight_hours_page.html', context)


def prosopiko_eksaminou(request):
    eksaminoi = Airman.objects.filter(
        flighthours__category="6ΜΗΝΟ").order_by('lastname').distinct()
    context = {'table_data': eksaminoi}
    return render(request, 'core/search_range/six_months.html', context)


def prosopiko_dekaotaminou(request):
    dekaoktaminoi = Airman.objects.filter(
        flighthours__category="18ΜΗΝΟ").order_by('lastname').distinct()
    context = {'table_data': dekaoktaminoi}
    return render(request, 'core/search_range/eighteen_months.html', context)


def trainers(request):
    trainers = AirmanTrainer.objects.all()
    context = {'table_data': trainers}
    return render(request, 'core/search_range/trainers.html', context)


def pilots(request):
    pilots = Airman.objects.filter(eidikotita="Ι").distinct()
    context = {'table_data': pilots}
    return render(request, 'core/search_range/ypa.html', context)


def search_range(request):
    if request.method == "POST":
        from_month = request.POST.get('from_month', None)
        from_year = request.POST.get('from_year', None)

        to_month = request.POST.get('to_month', None)
        to_year = request.POST.get('to_year', None)

        prosopiko = request.POST.get('prosopiko', None)

        if prosopiko == '6ΜΗΝΟ':
            results = FlightHours.objects.filter(
                category='6ΜΗΝΟ').order_by('airman__lastname')
        elif prosopiko == '18ΜΗΝΟ':
            results = FlightHours.objects.filter(
                category='18ΜΗΝΟ').order_by('airman__lastname')
        else:
            results = TrainHours.objects.all().order_by('airman__lastname')

        for hour in results:
            if not is_between(from_month, from_year, to_month, to_year, hour.month, hour.year):
                results = results.exclude(id=hour.id)

        context = {
            'table_data': results,
            'from_month': from_month,
            'from_year': from_year,
            'to_month': to_month,
            'to_year': to_year
        }

        if prosopiko == '6ΜΗΝΟ':
            return render(request, 'core/search_range/six_months.html', context)
        elif prosopiko == '18ΜΗΝΟ':
            return render(request, 'core/search_range/eighteen_months.html', context)
        elif prosopiko == 'TRAIN':
            return render(request, 'core/search_range/trainers.html', context)
        else:
            return render(request, 'core/search_range/ypa.html', context)

    context = {}
    return render(request, 'core/search_range/filter.html', context)


def add_flight_hour_suceess(request):
    context = {
        'success_message': 'Η ώρα πτήσης προστέθηκε.'
    }
    return render(request, 'core/eisagogi_dedomenon/add_flight_hour.html', context)


def add_flight_hour_exist(request):
    context = {
        'exist_message': 'Η ώρα πτήσης για τον ιπτάμενο για τον συγκεκριμένο μήνα και χρόνο υπάρχει ήδη.'
    }
    return render(request, 'core/eisagogi_dedomenon/add_flight_hour.html', context)


def add_flight_hour(request):
    if request.method == "POST":
        asma = request.POST.get('asma', None)
        lastname = request.POST.get('lastname', None)
        firstname = request.POST.get('firstname', None)
        rank = request.POST.get('rank', None)
        speciality = request.POST.get('speciality', None)
        plane = request.POST.get('plane', None)
        capthours = request.POST.get('capthours', 0)
        cocapthours = request.POST.get('cocapthours', 0)
        ifrhours = request.POST.get('ifrhours', 0)
        nighthours = request.POST.get('nighthours', 0)
        nauthours = request.POST.get('nauthours', 0)
        crewhours = request.POST.get('crewhours', 0)
        category = request.POST.get('category', None)
        unit = request.POST.get('unit', None)
        month = request.POST.get('month', None)
        year = request.POST.get('year', None)
        if asma == None:
            return redirect("/add/flightHour/")
        try:
            airman = Airman.objects.get(asma=asma)
        except:
            airman = Airman.objects.create(
                asma=asma,
                lastname=lastname,
                firstname=firstname,
                rank=rank,
                eidikotita=speciality
            )
        try:
            flighthour = FlightHours.objects.get(
                airman=airman,
                month=month,
                year=year
            )
            return HttpResponseRedirect(reverse('add_flight_hour_exist'))
        except:
            flighthour = FlightHours.objects.create(
                airman=airman,
                plane=plane,
                capthours=capthours,
                cocapthours=cocapthours,
                ifrhours=ifrhours,
                nighthours=nighthours,
                nauthours=nauthours,
                crewhours=crewhours,
                category=category,
                unit=unit,
                month=month,
                year=year
            )
        return HttpResponseRedirect(reverse('add_flight_hour_suceess'))
    else:
        return render(request, 'core/eisagogi_dedomenon/add_flight_hour.html')


def add_train_hour_suceess(request):
    context = {
        'success_message': 'Η ώρα εκπαίδευσης προστέθηκε.'
    }
    return render(request, 'core/eisagogi_dedomenon/eisagogi_ores_ekpaideutwn.html', context)


def add_train_hour_exist(request):
    context = {
        'exist_message': 'Η ώρα εκπαίδευσης για τον εκπαιδευτή για τον συγκεκριμένο μήνα, χρόνο και Α/Φ υπάρχει ήδη.'
    }
    return render(request, 'core/eisagogi_dedomenon/eisagogi_ores_ekpaideutwn.html', context)


def add_train_hour(request):
    if request.method == "POST":
        asma = request.POST.get('asma', None)
        lastname = request.POST.get('lastname', None)
        firstname = request.POST.get('firstname', None)
        rank = request.POST.get('rank', None)
        speciality = request.POST.get('speciality', None)
        plane = request.POST.get('plane', None)
        hours = request.POST.get('hours', 0)
        month = request.POST.get('month', None)
        year = request.POST.get('year', None)
        if asma == None:
            return redirect("/add/trainHour/")
        try:
            airman = Airman.objects.get(asma=asma)
        except:
            airman = Airman.objects.create(
                asma=asma,
                lastname=lastname,
                firstname=firstname,
                rank=rank,
                eidikotita=speciality
            )
        try:
            trainer = AirmanTrainer.objects.get(airman=airman)
        except:
            trainer = AirmanTrainer.objects.create(
                airman=airman
            )
        try:
            trainhour = TrainHours.objects.get(
                airman=airman,
                plane=plane,
                month=month,
                year=year
            )
            return HttpResponseRedirect(reverse('add_train_hour_exist'))
        except:
            trainhour = TrainHours.objects.create(
                airman=airman,
                plane=plane,
                hours=hours,
                month=month,
                year=year
            )
        return HttpResponseRedirect(reverse('add_train_hour_suceess'))
    else:
        return render(request, 'core/eisagogi_dedomenon/eisagogi_ores_ekpaideutwn.html')


def findasma(request):
    asma = request.GET.get('asma', None)
    try:
        airman = Airman.objects.get(asma=asma)
    except:
        airman = None

    if airman != None:
        response = {
            'found': True,
            'asma': airman.asma,
            'lastname': airman.lastname,
            'firstname': airman.firstname,
            'rank': airman.rank,
            'speciality': airman.eidikotita,
            'idiotita': airman.idiotita,
            'topothetisi': airman.topothetisi,
            'diathesimotita': airman.availability,
            'katigoria_dikaioumeni': airman.katigoria_dikaioumeni,
            'katigoria_katoxiromeni': airman.katigoria_katoxiromeni,
            'monada_ekdosis_ptitikou': airman.monada_ekdosis_ptitikou,
            'geniko_synolo_oron': airman.geniko_synolo_oron
        }
    else:
        response = {
            'found': False
        }
    return JsonResponse(response)


def train_hours(request):
    context = {}
    table_data = TrainHours.objects.all().order_by('airman__lastname')
    context = {'table_data': table_data}
    return render(request, 'core/train_hours_page.html', context)


def profile(request, asma):
    try:
        airman = Airman.objects.get(asma=asma)
        flight_hours = FlightHours.objects.filter(airman=airman)
        train_hours = TrainHours.objects.filter(airman=airman)
    except:
        return redirect('/')
    try:
        trainer = AirmanTrainer.objects.get(airman=airman)
    except:
        trainer = None

    context = {
        'pilot': airman,
        'trainer': trainer,
        'flight_hours': flight_hours,
        'train_hours': train_hours
    }
    return render(request, 'core/airman_profile.html', context)


def search(request):
    if request.method == "POST":
        asma = request.POST.get('asma', None)
        if asma != None:
            try:
                airman = Airman.objects.get(asma=asma)
            except:
                return redirect("/")
            url = "/profile/"+asma
            return redirect(url)

    return redirect("/")


def changetabledata(request):
    to_change = request.GET.get('to_change', None)
    value = request.GET.get('value', None)

    return HttpResponse(str(to_change))


def vevaiosi(request):
    context = {}
    return render(request, 'core/vevaioseis/vevaiosi_form.html', context)
