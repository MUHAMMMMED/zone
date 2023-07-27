
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
import datetime


from django.db.models import Sum

def handle_not_found(request, exception):
    return render(request, '404.html', status=404)

def handle_server_error(request):
    return render(request, '500.html', status=500)


#
# def handle_not_found(request, exception, web_slug):
#     web = WEB.objects.get(slug=web_slug)
#     if web.views_confirmation is None:
#         web.views_confirmation = 0
#     web.views_confirmation += 1
#     web.save()
#     booking = Appointment.objects.last()
#
#     return render(request, 'not-found.html', {'booking': booking, 'web': web})
#
#
#
#
#
#
#
#
# from django.views.decorators.csrf import requires_csrf_token
# from django.views import defaults as default_views
#
# @requires_csrf_token
# def handle_server_error(request, web_slug):
#     web = WEB.objects.get(slug=web_slug)
#     if web.views_confirmation is None:
#         web.views_confirmation = 0
#     web.views_confirmation += 1
#     web.save()
#     booking = Appointment.objects.last()
#
#     return default_views.server_error(request, template_name='not-found.html')


from django.http import JsonResponse
#
# def get_cart_item_count(request, web_slug):
#     web = get_object_or_404(WEB, slug=web_slug)
#     print('web',web)
#     # Get or create session
#     session_key = request.session.session_key
#     if not session_key:
#         request.session.save()
#         session_key = request.session.session_key
#
#     cart_item_count = CartItem.objects.filter(session_id=session_key, web=web).count()
#     data = {'count': cart_item_count}
#     return JsonResponse(data)






# # Create your views here.
def home(request):

    context = {}
    return render(request, 'home.html', context)
#
# def web(request, web_slug):
#     # Get the WEB object with the given slug
#     try:
#         web = get_object_or_404(WEB, slug=web_slug, active=True)
#         # Get all Categories objects for the current web object
#         doctors = Doctors.objects.filter(web=web)
#         section = Section.objects.filter(web=web)
#         insurance = Insurance.objects.filter(web=web)
#         image = Image.objects.filter(web=web)
#         questions = Questions.objects.filter(web=web)
#         department = Department.objects.filter(web=web)
#         categories = Categories.objects.filter(web=web, active=True)
#     except:
#         # Display an error message if the requested category or service does not exist
#         return render(request, 'error.html', {'message': 'The requested service could not be found.'})
#
#     # Create a dictionary to store the categories and their related services
#     category_services = {}
#     # Loop through each category and get its related services
#     for category in categories:
#         services = category.Services.filter(active=True)
#         for service in services:
#             if service.discount_percentage > 0:
#                 sale_price = service.price * (1 - service.discount_percentage / 100)
#                 service.sale_price = round(sale_price, 2)
#             else:
#                 service.sale_price = None
#             category_services[category] = services
#
#     # Process the booking form
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.web = web
#
#             # Check if patient with given phone number already exists
#             try:
#                 patient = Patient.objects.get(phone=order.phone)
#                 print('Patient already exists')
#                 order.ClientStatus = 'قديم'
#             except Patient.DoesNotExist:
#                 # If patient does not exist, create a new one
#                 patient = Patient.objects.create(
#                     phone=order.phone,
#                     name=order.name,
#                     web=web
#                 )
#                 print('Created new patient')
#                 order.ClientStatus = 'جديد'
#
#             # Set the patient for this appointment and save it
#             order.patient = patient
#             order.save()
#
#             print('Saved appointment for patient')
#
#             service_id = request.POST.get('service_id')
#             service = get_object_or_404(Service, id=service_id)
#             order.service=service
#
#             order.doctor_id=service.doctors
#             order.category_id=service.category_id
#
#             date = request.POST.get('id_date_' + str(service_id))
#             time_str = request.POST.get('id_time_' + str(service_id))
#             if time_str and date:
#                 # Convert Arabic "pm" or "am" to English "pm" or "am"
#                 time_str = time_str.replace('م', 'PM').replace('ص', 'AM')
#                 time = datetime.datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M:%S')
#                 order.date = date
#                 order.time = time
#                 order.save()
#                 print(time)
#             else:
#                 # Handle the case where the time string is empty
#
#                 print('Time string is empty')
#             order.save()
#             # Get the phone number from the form data
#             phone_number = form.cleaned_data['phone']
#             message = 'Your appointment has been scheduled for {} at {} with Dr. {}'.format(date, time, service.doctors)
#
#             # Get the current date and time in the timezone set in Django's settings
#
#             # print('web',web)
#             # print('service',service)
#             # update_booking_pixels(web, service)
#
#             # messages.success(request, 'تم إرسال طلب الحجز بنجاح.')
#             return redirect('webs:booking_confirmation', web_slug=web_slug)
#
#
#     else:
#         form = BookingForm()
#
#
#
#         # Get the current date and time in the timezone set in Django's settings
#         current_datetime = timezone.now()
#         # Get the Pixel object for the current date, or None if it doesn't exist
#         PIXEL = pixel.objects.filter(web=web, date=current_datetime.date()).first()
#         print('pixel', PIXEL)
#         if PIXEL is not None:
#             # If the Pixel object exists, increment the click_whatsapp_Allcategories field and save it
#             if PIXEL.views_Home is None:
#                 PIXEL.views_Home = 0
#             PIXEL.views_Home += 1
#             PIXEL.save()
#         else:
#             # If the Pixel object doesn't exist, create a new one with a click_whatsapp_Allcategories value of 1
#             PIXEL = pixel.objects.create(web=web, date=current_datetime.date(), views_Home=1)
#
#
#
#     context = {
#         'web': web,
#         'categories': categories,
#         'category_services': category_services,
#
#         'form': form,
#         'doctors': doctors,
#         'section': section,
#         'insurance': insurance,
#         'image': image,
#         'questions': questions,
#         'department': department,
#     }
#
#     # Render the web template with the web object
#     return render(request, 'WEb.html', context)
#


def web(request, web_slug):
    # Get the WEB object with the given slug
    try:
        web = get_object_or_404(WEB, slug=web_slug, active=True)
        # Get all Categories objects for the current web object
        doctors = Doctors.objects.filter(web=web)
        section = Section.objects.filter(web=web)
        insurance = Insurance.objects.filter(web=web)
        image = Image.objects.filter(web=web)
        questions = Questions.objects.filter(web=web)
        department = Department.objects.filter(web=web)
        categories = Categories.objects.filter(web=web, active=True)
    except:
        # Display an error message if the requested category or service does not exist
        return render(request, 'error.html', {'message': 'The requested service could not be found.'})

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

    # Process the booking form
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

        # Get the current date and time in the timezone set in Django's settings
        current_datetime = timezone.now()
        # Get the Pixel object for the current date, or None if it doesn't exist
        PIXEL = pixel.objects.filter(web=web, date=current_datetime.date()).first()
        print('pixel', PIXEL)
        if PIXEL is not None:
            # If the Pixel object exists, increment the click_whatsapp_Allcategories field and save it
            if PIXEL.views_Home is None:
                PIXEL.views_Home = 0
            PIXEL.views_Home += 1
            PIXEL.save()
        else:
            # If the Pixel object doesn't exist, create a new one with a click_whatsapp_Allcategories value of 1
            PIXEL = pixel.objects.create(web=web, date=current_datetime.date(), views_Home=1)



    context = {
        'web': web,
        'categories': categories,
        'category_services': category_services,

        'form': form,
        'doctors': doctors,
        'section': section,
        'insurance': insurance,
        'image': image,
        'questions': questions,
        'department': department,
    }

    # Render the web template with the web object
    return render(request, 'WEb.html', context)

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





import datetime
def pixel_data(request, web_slug):
    web = get_object_or_404(WEB, slug=web_slug)
    pixels = pixel.objects.filter(web=web)
    categories_pixel = Categories_pixel.objects.filter(web=web)
    service_pixel = Service_pixel.objects.filter(web=web)
    doctors_pixel = Doctors_pixel.objects.filter(web=web)

    # end_date = datetime.now().date() # Define end_date here

    context = {
        'categories_pixel': categories_pixel,
        'pixels': pixels,
        'service_pixel': service_pixel,
        'doctors_pixel': doctors_pixel,
    }

    # # Define the default date ranges
    # last_week = end_date - timedelta(days=7)
    # last_month = end_date - timedelta(days=30)
    #
    # if request.method == 'POST':
    #    start_date = request.POST.get('start_date')
    #    end_date = request.POST.get('end_date')
    # else:
    #     # If no dates are provided, use the last month as the default date range
    #     start_date = last_month
    #     end_date = end_date # Use the previously defined end_date
    #




    services = Service_pixel.objects.filter(web=web )
    service_stats = []
    for service in services:
        service_stat = {}
        service_stat['name'] = service.ServiceName
        service_stat['views'] = service.views
        service_stat['click_whatsapp'] = service.click_whatsapp
        service_stat['booking'] = service.booking
        service_stats.append(service_stat)
    context.update({'service_stats': service_stats})

    categories = Categories_pixel.objects.filter(web=web )
    categories_stats = []
    for category in categories:
        category_stat = {}
        category_stat['name'] = category.CategoryName
        category_stat['views'] = category.views
        category_stat['click_whatsapp'] = category.click_whatsapp
        category_stat['booking'] = category.booking
        categories_stats.append(category_stat)
    context.update({'categories_stats': categories_stats})

    doctors = Doctors_pixel.objects.filter(web=web )
    doctor_stats = []
    for doctor in doctors:
        doctor_stat = {}
        doctor_stat['name'] = doctor.DoctorName
        doctor_stat['views'] = doctor.views
        doctor_stat['click_whatsapp'] = doctor.click_whatsapp
        doctor_stat['booking'] = doctor.booking
        doctor_stats.append(doctor_stat)
    context.update({'doctor_stats': doctor_stats})

    pixel_data = pixel.objects.filter(web=web )
    pixel_stats = pixel_data.aggregate(
        Sum('views_Home'), Sum('click_whatsapp_Home'),
        Sum('views_Allcategories'), Sum('click_whatsapp_Allcategories'),
        Sum('views_Confirmation'), Sum('click_whatsapp_Doctor'),
        Sum('view_Doctor'), Sum('views_Link_page'))
    context.update({'pixel_stats': pixel_stats})

    return render(request, 'pixel_data.html', context)
