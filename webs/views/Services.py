
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
from django.utils import timezone

import datetime
import json
from decimal import Decimal
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404



#
# def services(request, web_slug, category_id, service_id):
#     # Define the formservice variable with an initial value
#     formservice = BookingForm()
#
#     try:
#         # Get the web object for the current request
#         # web = get_object_or_404(WEB, slug=web_slug)
#         web = get_object_or_404(WEB, slug=web_slug, active=True)
#         categories_nav = Categories.objects.filter(web=web)
#         # Get the category object for the current request
#         category = get_object_or_404(Categories, id=category_id, web=web)
#         # Get the service object for the current request
#         service = get_object_or_404(Service, id=service_id, active=True)
#
#         if service.discount_percentage > 0:
#             sale_price = service.price * (1 - service.discount_percentage / 100)
#             service.sale_price = round(sale_price, 2)
#         else:
#             service.sale_price = None
#
#         service.save()
#
#
#         # Get all other services in the same category
#         services_in_category = Service.objects.filter(category_id=category.id,active=True).exclude(id=service.id)
#
#
#     except:
#         # Display an error message if the requested category or service does not exist
#         return render(request, 'error.html', {'message': 'The requested service could not be found.'})


def services(request, web_slug, category_id, service_id):
    # Define the formservice variable with an initial value
    formservice = BookingForm()

    try:
        # Get the web object for the current request
        web = get_object_or_404(WEB, slug=web_slug)
        categories_nav = Categories.objects.filter(web=web)
        patients = Patient.objects.filter(web=web)

        # Get the category object for the current request
        category = get_object_or_404(Categories, id=category_id, web=web)
        # Get the service object for the current request
        service = get_object_or_404(Service, id=service_id, active=True)

        # Get all other services in the same category
        services_in_category = Service.objects.filter(category_id=category.id,active=True).exclude(id=service.id)
 
    except:
        # Display an error message if the requested category or service does not exist
        return render(request, 'error.html', {'message': 'The requested service could not be found.'})



    if 'card_service_submit' in request.POST:
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
                print(time)
            else:
                # Handle the case where the time string is empty
                print('Time string is empty')


            update_booking_pixels(web, service)
            return redirect('webs:booking_confirmation', web_slug=web_slug)

    elif 'service_submit' in request.POST:
       formservice = BookingForm(request.POST)  # Assign a new value to formservice
       if formservice.is_valid():
        # Save the booking and associate it with the current service
            order = formservice.save(commit=False)
            order.web = web # Set the web attribute of the booking object

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
            service_id=service


            order.service=service
            order.doctor_id=service.doctors
            order.category_id=service.category_id
            order.serviceName=service.Title

            if service.discount_percentage > 0:
                 order.price = service.price * (1 - service.discount_percentage / 100)
            else:
                 order.price = service.price
            order.save()
            date = request.POST.get('id_date_' + str(service_id.id))
            time_str = request.POST.get('id_time_' + str(service_id.id))
            if time_str and date:
                # Convert Arabic "pm" or "am" to English "pm" or "am"
                time_str = time_str.replace('م', 'PM').replace('ص', 'AM')
                time = datetime.datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M:%S')
                order.date = date
                order.time = time
                order.save()
                print(time)
            elif date:
                # Handle the case where the time string is empty
                print('Time string is empty')
                order.date = date
                order.save()
            else:
                # Handle the case where the date is empty
                print('Date string is empty')

            order.patient = patient


            order.save()
            update_booking_pixels(web, service)


            # Redirect the user to a confirmation page or some other view
            return redirect('webs:booking_confirmation', web_slug=web_slug)

    else:
        # Display an empty booking form
        form = BookingForm()

    current_datetime = timezone.now()
        # Get the Pixel object for the current date, or None if it doesn't exist
    Service_PIXEL = Service_pixel.objects.filter(ServiceName=service.Title ,   web=web, date=current_datetime.date()).first()
    print('Service_PIXEL', Service_PIXEL)
    if Service_PIXEL is not None:
            # If the Pixel object exists, increment the click_whatsapp_Allcategories field and save it
            if Service_PIXEL.views is None:
                Service_PIXEL.views = 0
            Service_PIXEL.views += 1
            Service_PIXEL.ServiceName=service.Title
            Service_PIXEL.save()
            print('if ' )
    else:
            # If the Pixel object doesn't exist, create a new one with a click_whatsapp_Allcategories value of 1
            PIXEL = Service_pixel.objects.create(web=web,ServiceName=service.Title , date=current_datetime.date(), views=1)
            print('else' )
    # rest of the code
    # ... render the service detail template with the updated service object ...




    context = {
        'web': web,
        'category': category,
        'service': service,
        'services_in_category': services_in_category,
        'form': form,
        'formservice': formservice,
        'categories_nav': categories_nav,

    }
    return render(request, 'salh.html', context)




#
#
# def services(request, web_slug, category_id, service_id):
#     # Define the formservice variable with an initial value
#     # formservice = BookingForm()
#
#     try:
#         # Get the web object for the current request
#         # web = get_object_or_404(WEB, slug=web_slug)
#         web = get_object_or_404(WEB, slug=web_slug, active=True)
#         categories_nav = Categories.objects.filter(web=web)
#         # Get the category object for the current request
#         category = get_object_or_404(Categories, id=category_id, web=web)
#         # Get the service object for the current request
#         service = get_object_or_404(Service, id=service_id, active=True)
#
#         # Get all other services in the same category
#         services_in_category = Service.objects.filter(category_id=category.id,active=True).exclude(id=service.id)
#         # for service in services_in_category:
#         #         if service.discount_percentage > 0:
#         #             sale_price = service.price * (1 - service.discount_percentage / 100)
#         #             service.sale_price = round(sale_price, 2)
#         #         else:
#         #             service.sale_price = None
#
#     except:
#         # Display an error message if the requested category or service does not exist
#         return render(request, 'error.html', {'message': 'The requested service could not be found.'})
    #
    #
    # if 'card_service_submit' in request.POST:
    #     form = BookingForm(request.POST)
    #     if form.is_valid():
    #         order = form.save(commit=False)
    #         order.web = web
    #
    #         # Check if patient with given phone number already exists
    #         try:
    #             patient = Patient.objects.get(phone=order.phone)
    #             print('Patient already exists')
    #             order.ClientStatus = 'قديم'
    #         except Patient.DoesNotExist:
    #             # If patient does not exist, create a new one
    #             patient = Patient.objects.create(
    #                 phone=order.phone,
    #                 name=order.name,
    #                 web=web
    #             )
    #             print('Created new patient')
    #             order.ClientStatus = 'جديد'
    #
    #         # Set the patient for this appointment and save it
    #         order.patient = patient
    #         order.save()
    #         print('Saved appointment for patient')
    #
    #         service_id = request.POST.get('service_id')
    #         service = get_object_or_404(Service, id=service_id)
    #         order.service=service
    #         order.doctor_id=service.doctors
    #         order.category_id=service.category_id
    #         date = request.POST.get('id_date_' + str(service_id))
    #         time_str = request.POST.get('id_time_' + str(service_id))
    #         if time_str and date:
    #             # Convert Arabic "pm" or "am" to English "pm" or "am"
    #             time_str = time_str.replace('م', 'PM').replace('ص', 'AM')
    #             time = datetime.datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M:%S')
    #             order.date = date
    #             order.time = time
    #             order.save()
    #             print(time)
    #         else:
    #             # Handle the case where the time string is empty
    #             print('Time string is empty')
    #
    #         order.service
    #         order.save()
    #         return redirect('webs:booking_confirmation', web_slug=web_slug)
    # #
    # elif 'service_submit' in request.POST:
    #    formservice = BookingForm(request.POST)  # Assign a new value to formservice
    #    if formservice.is_valid():
    #     # Save the booking and associate it with the current service
    #         order = formservice.save(commit=False)
    #
    #         order.web = web # Set the web attribute of the booking object
    #
    #
    #         # Check if patient with given phone number already exists
    #         try:
    #             patient = Patient.objects.get(phone=order.phone)
    #             print('Patient already exists')
    #             order.ClientStatus = 'قديم'
    #         except Patient.DoesNotExist:
    #             # If patient does not exist, create a new one
    #             patient = Patient.objects.create(
    #                 phone=order.phone,
    #                 name=order.name,
    #                 web=web
    #             )
    #             print('Created new patient')
    #             order.ClientStatus = 'جديد'
    #
    #
    #         # Set the patient for this appointment and save it
    #         service_id=service
    #         order.service=service_id
    #         order.doctor_id=service_id.doctors
    #         order.category_id=service_id.category_id
    #         date = request.POST.get('id_date_' + str(service_id.id))
    #         time_str = request.POST.get('id_time_' + str(service_id.id))
    #         if time_str and date:
    #             # Convert Arabic "pm" or "am" to English "pm" or "am"
    #             time_str = time_str.replace('م', 'PM').replace('ص', 'AM')
    #             time = datetime.datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M:%S')
    #             order.date = date
    #             order.time = time
    #             order.save()
    #             print(time)
    #         elif date:
    #             # Handle the case where the time string is empty
    #             print('Time string is empty')
    #             order.date = date
    #             order.save()
    #         else:
    #             # Handle the case where the date is empty
    #             print('Date string is empty')
    #
    #         order.patient = patient
    #
    #
    #         order.save()
    #         # Redirect the user to a confirmation page or some other view
    #         return redirect('webs:booking_confirmation', web_slug=web_slug)
    #
    # else:
    #     # Display an empty booking form
    #     form = BookingForm()
    # current_datetime = timezone.now()
    #     # Get the Pixel object for the current date, or None if it doesn't exist
    # Service_PIXEL = Service_pixel.objects.filter(ServiceName=service.Title ,   web=web, date=current_datetime.date()).first()
    # print('Service_PIXEL', Service_PIXEL)
    # if Service_PIXEL is not None:
    #         # If the Pixel object exists, increment the click_whatsapp_Allcategories field and save it
    #         if Service_PIXEL.views is None:
    #             Service_PIXEL.views = 0
    #         Service_PIXEL.views += 1
    #         Service_PIXEL.ServiceName=service.Title
    #         Service_PIXEL.save()
    #         print('if ' )
    # else:
    #         # If the Pixel object doesn't exist, create a new one with a click_whatsapp_Allcategories value of 1
    #         PIXEL = Service_pixel.objects.create(web=web,ServiceName=service.Title , date=current_datetime.date(), views=1)
    #         print('else' )
    # rest of the code
    # ... render the service detail template with the updated service object ...
    # context = {
    #     'web': web,
    #     'category': category,
    #     'service': service,
    #     'services_in_category': services_in_category,
    #     # 'form': form,
    #     # 'formservice': formservice,
    #     'categories_nav': categories_nav,
    #
    # }
    # return render(request, 'salh.html', context)
    #










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
