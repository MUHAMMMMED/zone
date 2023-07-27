
from webs.models import *
from webs.BaseData_processors import *
import pandas as pd
from webs.form import *
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.sessions.backends.db import SessionStore
from webs.models import *
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
import datetime
import json
from decimal import Decimal
from django.utils import timezone
from datetime import date

# web




def increment_click_web_whatsapp(request, web_slug):
    try:
        web = get_object_or_404(WEB, slug=web_slug, active=True)
        print('web',web)
        # Get the current date and time in the timezone set in Django's settings
        current_datetime = timezone.now()
        # Get the Pixel object for the current date, or None if it doesn't exist
        PIXEL = pixel.objects.filter(web=web, date=current_datetime.date()).first()
        print('pixel', PIXEL)
        if PIXEL is not None:
            # If the Pixel object exists, increment the click_whatsapp_Allcategories field and save it
            if PIXEL.click_whatsapp_Home is None:
                PIXEL.click_whatsapp_Home = 0
            PIXEL.click_whatsapp_Home += 1
            PIXEL.save()
        else:
            # If the Pixel object doesn't exist, create a new one with a click_whatsapp_Allcategories value of 1
            PIXEL = pixel.objects.create(web=web, date=current_datetime.date(), click_whatsapp_Home=1)
        return JsonResponse({'click_whatsapp': PIXEL.click_whatsapp_Home})
    except WEB.DoesNotExist:
        return JsonResponse({'error': 'WEB not found'}, status=404)



# category





def increment_click_category_whatsapp(request, category_id,web_slug):
    try:
        web = get_object_or_404(WEB, slug=web_slug, active=True)
        category = get_object_or_404(Categories, id=category_id, web=web)
        print('web',web)
        print('category',category)
        # Get the current date and time in the timezone set in Django's settings
        current_datetime = timezone.now()
        # Get the Pixel object for the current date, or None if it doesn't exist
        PIXEL = Categories_pixel.objects.filter(web=web, CategoryName=category.Name, date=current_datetime.date()).first()

        print('pixel', PIXEL)
        if PIXEL is not None:
            if PIXEL.click_whatsapp is None:
                PIXEL.click_whatsapp = 0
            PIXEL.click_whatsapp += 1
            PIXEL.CategoryName=category.Name
            PIXEL.save()
        else:
            # If the Pixel object doesn't exist, create a new one with a click_whatsapp_Allcategories value of 1
            PIXEL = Categories_pixel.objects.create(web=web,CategoryName=category.Name, date=current_datetime.date(), click_whatsapp=1)
        return JsonResponse({'click_whatsapp': PIXEL.click_whatsapp})
    except web.DoesNotExist:
        return JsonResponse({'error': 'WEB not found'}, status=404)














def increment_click_all_category_whatsapp(request, web_slug):
    try:
        web = get_object_or_404(WEB, slug=web_slug, active=True)
        print('web',web)
        # Get the current date and time in the timezone set in Django's settings
        current_datetime = timezone.now()
        # Get the Pixel object for the current date, or None if it doesn't exist
        PIXEL = pixel.objects.filter(web=web, date=current_datetime.date()).first()

        if PIXEL is not None:
            # If the Pixel object exists, increment the click_whatsapp_Allcategories field and save it
            if PIXEL.click_whatsapp_Allcategories is None:
                PIXEL.click_whatsapp_Allcategories = 0
            PIXEL.click_whatsapp_Allcategories += 1
            PIXEL.save()
        else:
            # If the Pixel object doesn't exist, create a new one with a click_whatsapp_Allcategories value of 1
            PIXEL = pixel.objects.create(web=web, date=current_datetime.date(), click_whatsapp_Allcategories=1)
        return JsonResponse({'click_whatsapp': PIXEL.click_whatsapp_Allcategories})
    except WEB.DoesNotExist:
        return JsonResponse({'error': 'WEB not found'}, status=404)


# Doctors

def increment_click_Doctors_whatsapp(request, web_slug):
    try:
        web = get_object_or_404(WEB, slug=web_slug, active=True)
        print('web',web)
        # Get the current date and time in the timezone set in Django's settings
        current_datetime = timezone.now()
        # Get the Pixel object for the current date, or None if it doesn't exist
        PIXEL = pixel.objects.filter(web=web, date=current_datetime.date()).first()
        print('pixel', PIXEL)
        if PIXEL is not None:
            # If the Pixel object exists, increment the click_whatsapp_Allcategories field and save it
            if PIXEL.click_whatsapp_Doctor is None:
                PIXEL.click_whatsapp_Doctor = 0
            PIXEL.click_whatsapp_Doctor += 1
            PIXEL.save()
        else:
            # If the Pixel object doesn't exist, create a new one with a click_whatsapp_Allcategories value of 1
            PIXEL = pixel.objects.create(web=web, date=current_datetime.date(), click_whatsapp_Doctor=1)
        return JsonResponse({'click_whatsapp': PIXEL.click_whatsapp_Doctor})
    except WEB.DoesNotExist:
        return JsonResponse({'error': 'WEB not found'}, status=404)





def increment_click_Doctors_details_whatsapp(request, doctor_id, web_slug):
    try:
        web = get_object_or_404(WEB, slug=web_slug, active=True)
        doctor = get_object_or_404(Doctors, id=doctor_id, web=web)
        print('web',web)
        print('doctor',doctor)
        # Get the current date and time in the timezone set in Django's settings
        current_datetime = timezone.now()
        # Get the Pixel object for the current date, or None if it doesn't exist
        PIXEL = Doctors_pixel.objects.filter(web=web, DoctorName=doctor.Name, date=current_datetime.date()).first()

        print('pixel', PIXEL)
        if PIXEL is not None:
            if PIXEL.click_whatsapp is None:
                PIXEL.click_whatsapp = 0
            PIXEL.click_whatsapp += 1
            PIXEL.DoctorName=doctor.Name
            PIXEL.save()
        else:
            # If the Pixel object doesn't exist, create a new one with a click_whatsapp_Allcategories value of 1
            PIXEL = Doctors_pixel.objects.create(web=web, DoctorName=doctor.Name, date=current_datetime.date(), click_whatsapp=1)
        return JsonResponse({'click_whatsapp': PIXEL.click_whatsapp})
    except web.DoesNotExist:
        return JsonResponse({'error': 'WEB not found'}, status=404)






# service


def increment_click_service_whatsapp(request, service_id, web_slug):
    try:
        web = get_object_or_404(WEB, slug=web_slug, active=True)
        print('web', web)
        print('service_id', service_id)
        # Get the current date and time in the timezone set in Django's settings
        current_datetime = timezone.now()
        # Get the Pixel object for the current date, or None if it doesn't exist
        service = get_object_or_404(Service, id=service_id, web=web, active=True)
        PIXEL = Service_pixel.objects.filter(ServiceName=service.Title, web=web, date=current_datetime.date()).first()
        print('pixel', PIXEL)
        if PIXEL is not None:
            if PIXEL.click_whatsapp is None:
                PIXEL.click_whatsapp = 0
            PIXEL.click_whatsapp += 1
            PIXEL.ServiceName =service.Title
            PIXEL.save()
        else:
            # If the Pixel object doesn't exist, create a new one with a click_whatsapp_Allcategories value of 1
            PIXEL = Service_pixel.objects.create(web=web,ServiceName = service.Title, date=current_datetime.date(), click_whatsapp=1)
        return JsonResponse({'click_whatsapp': PIXEL.click_whatsapp})
    except web.DoesNotExist:
        return JsonResponse({'error': 'WEB not found'}, status=404)
