
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

def view_links(request, web_slug):

    try:
       web = get_object_or_404(WEB, slug=web_slug, active=True)
       links = Link.objects.filter(web=web)
    except:
        # Display an error message if the requested category or service does not exist
        return render(request, 'error.html', {'message': 'The requested service could not be found.'})
        # Get the current date and time in the timezone set in Django's settings
    current_datetime = timezone.now()
        # Get the Pixel object for the current date, or None if it doesn't exist
    PIXEL = pixel.objects.filter(web=web, date=current_datetime.date()).first()
    print('pixel', PIXEL)
    if PIXEL is not None:
            # If the Pixel object exists, increment the click_whatsapp_Allcategories field and save it
            if PIXEL.views_Link_page is None:
                PIXEL.views_Link_page = 0
            PIXEL.views_Link_page += 1
            PIXEL.save()
    else:
            # If the Pixel object doesn't exist, create a new one with a click_whatsapp_Allcategories value of 1
            PIXEL = pixel.objects.create(web=web, date=current_datetime.date(), views_Link_page=1)




    context = {
        'web': web,
        'links': links
    }
    return render(request, 'link.html', context)
