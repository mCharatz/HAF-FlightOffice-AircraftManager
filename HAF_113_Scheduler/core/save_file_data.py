from django.shortcuts import redirect
from .models import *
import logging
import copy


def save_data(data, month=None, year=None):
    if month == None or year == None:
        for_flightgours(data)
        return redirect("/add/uploadFile/success")
    else:
        for_trainhours(data, month, year)
        return redirect("/add/uploadFile/success")
    return True


def replace(str1):
    maketrans = str1.maketrans
    final = str1.translate(maketrans(',.', '.,', ' '))
    if final == "":
        return "0"
    return final.replace(',', ", ")


def for_flightgours(flighthours):
    try:
        for flighthour in flighthours:
            if len(flighthour[1]) != 16:
                continue
            flighthour[1][6] = replace(flighthour[1][6])
            flighthour[1][7] = replace(flighthour[1][7])
            flighthour[1][8] = replace(flighthour[1][8])
            flighthour[1][9] = replace(flighthour[1][9])
            flighthour[1][10] = replace(flighthour[1][10])
            flighthour[1][11] = replace(flighthour[1][11])
            try:
                airman_item = Airman.objects.get(asma=flighthour[1][0])
                airman_item.lastname = flighthour[1][1]
                airman_item.firstname = flighthour[1][2]
                airman_item.rank = flighthour[1][3]
                airman_item.eidikotita = flighthour[1][4]
                airman_item.save()
            except:
                airman_item = Airman.objects.create(
                    asma=flighthour[1][0],
                    lastname=flighthour[1][1],
                    firstname=flighthour[1][2],
                    rank=flighthour[1][3],
                    eidikotita=flighthour[1][4]
                )
            try:
                flight_hour_item = FlightHours.objects.get(
                    airman=airman_item,
                    unit=flighthour[1][13],
                    month=flighthour[1][14],
                    year=flighthour[1][15]
                )
            except:
                FlightHours.objects.create(
                    airman=airman_item,
                    plane=flighthour[1][5],
                    capthours=flighthour[1][6],
                    cocapthours=flighthour[1][7],
                    ifrhours=flighthour[1][8],
                    nighthours=flighthour[1][9],
                    nauthours=flighthour[1][10],
                    crewhours=flighthour[1][11],
                    category=flighthour[1][12],
                    unit=flighthour[1][13],
                    month=flighthour[1][14],
                    year=flighthour[1][15]
                )
    except:
        return False
    return True


def for_trainhours(trainhours, month, year):
    logger = logging.getLogger("mylogger")
    for trainhour in trainhours:
        if len(trainhour[1]) != 5:
            continue
        try:
            trainhour[1][4] = replace(trainhour[1][4])
        except:
            continue

        try:
            airman_item = Airman.objects.get(asma=trainhour[1][2])
            airman_item.lastname = trainhour[1][1]
            airman_item.rank = trainhour[1][0]
            airman_item.save()
        except:
            airman_item = Airman.objects.create(
                asma=trainhour[1][2],
                lastname=trainhour[1][1],
                rank=trainhour[1][0]
            )
        try:
            airman_trainer = AirmanTrainer.objects.get(asma=airman_item)
        except:
            airman_trainer = AirmanTrainer.objects.create(
                airman=airman_item
            )
        try:
            flight_hour_item = TrainHours.objects.get(
                airman=airman_item,
                month=month,
                year=year
            )
        except:
            TrainHours.objects.create(
                airman=airman_item,
                plane=trainhour[1][3],
                hours=trainhour[1][4],
                month=month,
                year=year
            )
    return True
