
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
from django.http import JsonResponse



import datetime
import json
from decimal import Decimal
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone




def categories_services(request, web_slug):
    try:
        # Get the web object for the current request
        web = get_object_or_404(WEB, slug=web_slug, active=True)
        # Get all Categories objects for the current web object
        categories_nav = Categories.objects.filter(web=web, active=True)
        categories = Categories.objects.filter(web=web, active=True)

        # Create a dictionary to store the categories and their related services
        category_services = {}
        # Loop through each category and get its related services
        for category in categories:
            services = category.Services.filter(active=True)
            for service in services:
                if service.discount_percentage > 0:
                    sale_price = service.price * (1 - service.discount_percentage / 100)
                    service.sale_price = round(sale_price, 2)
                else:
                    service.sale_price = None
            category_services[category] = services

    except:
        # Display an error message if the requested category or service does not exist
        return render(request, 'error.html', {'message': 'The requested service could not be found.'})

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.web = web

            # Check if patient with given phone number already exists
            try:
                patient = Patient.objects.get(phone=order.phone)
                print('Patient already exists')
                order.ClientStatus = 'قديم'
            except Patient.DoesNotExist:
                # If patient does not exist, create a new one
                patient = Patient.objects.create(
                    phone=order.phone,
                    name=order.name,
                    web=web
                )
                print('Created new patient')
                order.ClientStatus = 'جديد'

            # Set the patient for this appointment and save it
            order.patient = patient
            order.save()



            print('Saved appointment for patient')


            service_id = request.POST.get('service_id')
            service = get_object_or_404(Service, id=service_id)
            order.service=service
            order.doctor_id=service.doctors
            order.category_id=service.category_id
            order.serviceName=service.Title

            if service.discount_percentage > 0:
                 order.price = service.price * (1 - service.discount_percentage / 100)
            else:
                 order.price = service.price
            order.save()
            date = request.POST.get('id_date_' + str(service_id))
            time_str = request.POST.get('id_time_' + str(service_id))
            if time_str and date:
                # Convert Arabic "pm" or "am" to English "pm" or "am"
                time_str = time_str.replace('م', 'PM').replace('ص', 'AM')
                time = datetime.datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M:%S')
                order.date = date
                order.time = time
                order.save()

            else:
                # Handle the case where the time string is empty
                print('Time string is empty')

            # update_booking_pixels(web, service)
            # messages.success(request, 'تم إرسال طلب الحجز بنجاح.')
            return redirect('webs:booking_confirmation', web_slug=web_slug)


    else:
        form = BookingForm()


    current_datetime = timezone.now()
        # Get the Pixel object for the current date, or None if it doesn't exist
    PIXEL = pixel.objects.filter(web=web, date=current_datetime.date()).first()
    print('pixel', PIXEL)
    if PIXEL is not None:
            # If the Pixel object exists, increment the click_whatsapp_Allcategories field and save it
            if PIXEL.views_Allcategories is None:
                PIXEL.views_Allcategories = 0
            PIXEL.views_Allcategories += 1
            PIXEL.save()
    else:
            # If the Pixel object doesn't exist, create a new one with a click_whatsapp_Allcategories value of 1
            PIXEL = pixel.objects.create(web=web, date=current_datetime.date(), views_Allcategories=1)
    # Render the categories_services template with the category_services dictionary
    return render(request, 'categories_services.html', {'category_services': category_services,

                                                        'web': web,
                                                        'form': form,
                                                        'categories_nav': categories_nav})









def categories(request, web_slug, id):
    try:
        web = get_object_or_404(WEB, slug=web_slug, active=True)
        category = get_object_or_404(Categories, id=id, web=web, active=True)
        categories_nav = Categories.objects.filter(web=web, active=True)
        services = category.Services.filter(active=True)
    except:
        # Display an error message if the requested category or service does not exist
        return render(request, 'error.html', {'message': 'The requested service could not be found.'})

    for service in services:
        if service.discount_percentage > 0:
            sale_price = service.price * (1 - service.discount_percentage / 100)
            service.sale_price = round(sale_price, 2)
        else:
            service.sale_price = None

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.web = web

            # Check if patient with given phone number already exists
            try:
                patient = Patient.objects.get(phone=order.phone)
                print('Patient already exists')
                order.ClientStatus = 'قديم'
            except Patient.DoesNotExist:
                # If patient does not exist, create a new one
                patient = Patient.objects.create(
                    phone=order.phone,
                    name=order.name,
                    web=web
                )
                print('Created new patient')
                order.ClientStatus = 'جديد'

            # Set the patient for this appointment and save it
            order.patient = patient
            order.save()

            print('Saved appointment for patient')
 
            service_id = request.POST.get('service_id')
            service = get_object_or_404(Service, id=service_id)
            order.service=service
            order.doctor_id=service.doctors
            order.category_id=service.category_id
            order.serviceName=service.Title

            if service.discount_percentage > 0:
                 order.price = service.price * (1 - service.discount_percentage / 100)
            else:
                 order.price = service.price
            order.save()
            date = request.POST.get('id_date_' + str(service_id))
            time_str = request.POST.get('id_time_' + str(service_id))

            if time_str and date:
                # Convert Arabic "pm" or "am" to English "pm" or "am"
                time_str = time_str.replace('م', 'PM').replace('ص', 'AM')
                time = datetime.datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M:%S')
                order.date = date
                order.time = time
                order.save()

            else:
                # Handle the case where the time string is empty
                print('Time string is empty')

            update_booking_pixels(web, service)

            # messages.success(request, 'تم إرسال طلب الحجز بنجاح.')
            return redirect('webs:booking_confirmation', web_slug=web_slug)

    else:
        form = BookingForm()

    current_datetime = timezone.now()
        # Get the Pixel object for the current date, or None if it doesn't exist
    PIXEL = Categories_pixel.objects.filter( CategoryName=category.Name,web=web, date=current_datetime.date()).first()
    print('pixel', PIXEL)
    if PIXEL is not None:
            # If the Pixel object exists, increment the click_whatsapp_Allcategories field and save it
            if PIXEL.views is None:
                PIXEL.views = 0
            PIXEL.views += 1
            PIXEL.CategoryName=category.Name
            PIXEL.save()
    else:
            # If the Pixel object doesn't exist, create a new one with a click_whatsapp_Allcategories value of 1
            PIXEL = Categories_pixel.objects.create(web=web,CategoryName=category.Name , date=current_datetime.date(), views=1)

    return render(request, 'categories.html', {'category': category, 'web': web, 'categories_nav': categories_nav, 'form': form, 'services': services})




import datetime

              # update_booking_pixels(web, service)
def update_booking_pixels(web, service):
     current_datetime = datetime.datetime.now().date()

     Service_PIXEL = Service_pixel.objects.filter(ServiceName=service.Title, web=web, date=current_datetime).first()

     if Service_PIXEL is not None:

             if Service_PIXEL.booking is None:
                 Service_PIXEL.booking = 0
             Service_PIXEL.booking += 1
             Service_PIXEL.ServiceName=service.Title
             Service_PIXEL.save()
     else:

             Service_PIXEL = Service_pixel.objects.create(web=web,ServiceName=service.Title, date=current_datetime, booking=1)

     Doctors_PIXEL = Doctors_pixel.objects.filter(DoctorName=service.doctors.Name, web=web, date=current_datetime).first()

     if Doctors_PIXEL is not None:

              if Doctors_PIXEL.booking is None:
                  Doctors_PIXEL.booking = 0
              Doctors_PIXEL.booking += 1
              Doctors_PIXEL.DoctorName=service.doctors.Name
              Doctors_PIXEL.save()
     else:

              Doctors_PIXEL = Doctors_pixel.objects.create(web=web,DoctorName=service.doctors.Name, date=current_datetime, booking=1)

     Categories_PIXEL = Categories_pixel.objects.filter(CategoryName=service.category_id.Name, web=web, date=current_datetime).first()

     if Categories_PIXEL is not None:

              if Categories_PIXEL.booking is None:
                  Categories_PIXEL.booking = 0
              Categories_PIXEL.booking += 1
              Categories_PIXEL.CategoryName=service.category_id.Name
              Categories_PIXEL.save()
     else:

              Categories_PIXEL = Categories_pixel.objects.create(web=web,CategoryName=service.category_id.Name,date=current_datetime, booking=1)
