
from webs.models import *
from webs.BaseData_processors import *
import pandas as pd
from webs.form import *
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.sessions.backends.db import SessionStore
from webs.models import WEB, Service, Doctors, DoctorSchedule, Appointment
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



import datetime
import json
from decimal import Decimal
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone

def booking_confirmation(request, web_slug):
    # Get the last booking object created

    web = WEB.objects.get(slug=web_slug)
    if web.views_confirmation is None:
        web.views_confirmation = 0
    web.views_confirmation += 1
    web.save()
    booking = Appointment.objects.last()
    # Render the booking confirmation template with the booking ID and web slug

    current_datetime = timezone.now()
        # Get the Pixel object for the current date, or None if it doesn't exist
    PIXEL = pixel.objects.filter(web=web, date=current_datetime.date()).first()
    print('pixel', PIXEL)
    if PIXEL is not None:
            # If the Pixel object exists, increment the click_whatsapp_Allcategories field and save it
            if PIXEL.views_Confirmation is None:
                PIXEL.views_Confirmation = 0
            PIXEL.views_Confirmation += 1
            PIXEL.save()
    else:
            # If the Pixel object doesn't exist, create a new one with a click_whatsapp_Allcategories value of 1
            PIXEL = pixel.objects.create(web=web, date=current_datetime.date(), views_Confirmation=1)

    return render(request, 'booking_confirmation.html', {'booking': booking, 'web': web})
