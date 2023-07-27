# import os


import datetime as dt
from collections import defaultdict
import calendar


from webs.models import *
from Dashboard.forms import *
from webs.form import *
from Dashboard.filters import *
# # Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

import calendar
from collections import defaultdict
from django.db.models import Q
from django.db.models import Count
# from django.db.models import F
from django.utils import timezone
from django.conf import settings
from django.db.models.functions import StrIndex
from calendar import monthrange
import json
import pytz
from datetime import date, datetime, timedelta




@csrf_exempt
def create_nwe_appointment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        appointment = Appointment.objects.create(
            name=data['name'],
            phone=data['phone'],
            knew_from=data['knew_from'],
            note=data['note']
        )
        # Add services to the appointment
        services = data.get('services', [])
        for service_id in services:
            appointment.service.add(service_id)

        return JsonResponse({'success': True, 'appointment_id': appointment.id})
    else:
        return JsonResponse({'success': False})


def NewBooking(request):
    user = request.user
    web = WEB.objects.filter(Employee_WEB=user).first() # get the first WEB object
    categories = Categories.objects.filter(web__Employee_WEB=user, active=True)
    CartIte = CartIteInside.objects.filter(web=web) # filter CartIteInside objects directly based on the user parameter

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


    if request.method == 'POST':
        # Create a new booking object and add the cart items to it
        form = AppointmentForm(request.POST)
        if form.is_valid():
            booking =form.save(commit=False)
            booking.web = web
            phone_number = booking.phone

            if Appointment.objects.filter(web=web, phone=phone_number).exists():
                print('Phone number already exists')
                booking.ClientStatus = 'قديم'
            else:
                print('Phone number does not exist')
                booking.ClientStatus = 'جديد'


            booking.save()
            for cart_item in CartIte:
                booking.service.add(cart_item.service)

            # Delete the cart items for the current session and web
            CartIte.delete()
            return redirect('Dashboard:Appointment_waiting')
    else:
        form = AppointmentForm()

    return render(request, 'NewBooking.html', {'category_services': category_services, 'web': web, 'CartIte':CartIte,'form':form})



def update_appointment(request, id):
    web = WEB.objects.get(Employee_WEB=request.user)
    appointment = Appointment.objects.filter(web=web, id=id).first()
    # Access the appointment attributes
    service_id = None
    if appointment.service:
        service_id = appointment.service.id

    if request.method == 'POST':
        form = update_AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            date = request.POST.get('id_date')
            time_str = request.POST.get('id_time')
            if time_str and date:
                # Convert Arabic "pm" or "am" to English "pm" or "am"
                        time_str = time_str.replace('م', 'PM').replace('ص', 'AM')
                        time = datetime.datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M:%S')
                        appointment.date = date
                        appointment.time = time
                        appointment.save()
                        return redirect('Dashboard:Appointment_waiting')
            else:
                # Handle the case where the time string is empty
                print('Time string is empty')
                appointment.save()
                return redirect('Dashboard:Appointment_waiting')

    else:
        form = update_AppointmentForm(instance=appointment)

    context = {
        'form': form,
        'appointment': appointment,
        'service': service_id,
        'web': web.slug
    }
    return render(request, 'update_appointment.html', context)





def delete_service(request, service_id, appointment_id):
    user = request.user
    appointment = get_object_or_404(Appointment, id=appointment_id, web__Employee_WEB=user)
    service = get_object_or_404(Service, id=service_id)
    appointment.service.remove(service)
    return redirect('Dashboard:Appointment_waiting')





@login_required
def Appointment_waiting(request):
   user = request.user
   weB = WEB.objects.filter(Employee_WEB=user).first()
   categories = Categories.objects.filter(web__Employee_WEB=user)
   services = Service.objects.filter(category_id__in=categories)
   appointments = Appointment.objects.filter(web__Employee_WEB=user, status_appointment='انتظار')
   booking_filter = BookingFilter(request.GET, queryset=appointments)

     # Count appointments by status
   count_waiting = appointments.count()
 # .first()
   if weB:
       currency_name = weB.currencyـname
   else:
       currency_name = None


   title = 'انتظار'
   context = {
    'title': title,
    'Bookingfilter': booking_filter,
    'web':weB,
     'services': services,
     'Appointment':appointments,
    # count
    'count_waiting': count_waiting,
   }
   return render(request, 'waiting.html', context)


from datetime import datetime

@login_required
def Appointment_inquiries(request):
  user = User.objects.get(id=request.user.id)
  weB = WEB.objects.filter(Employee_WEB=user).first()
  booking = Appointment.objects.filter(web__Employee_WEB=user,status_appointment='inquiries')
  Bookingfilter = BookingFilter(request.GET, queryset=booking)
     # Count appointments by status
  count_inquiries = booking.count()
  if weB:
       currency_name = weB.currencyـname
  else:
       currency_name = None



  title='الاستفسار'
  context = {
  'title':title ,
  'Bookingfilter': Bookingfilter ,
   'web':weB,
  # count

  'count_inquiries':count_inquiries,

  }
  return render(request, 'waiting.html', context)




@login_required
def Appointment_notanswering(request):
  user = User.objects.get(id=request.user.id)
  weB = WEB.objects.filter(Employee_WEB=user).first()
  booking = Appointment.objects.filter(web__Employee_WEB=user,status_appointment='notanswering')
  Bookingfilter = BookingFilter(request.GET, queryset=booking)
  #
  #    # Count appointments by status
  count_notanswering = booking.count()
 # .first()
  if weB:
       currency_name = weB.currencyـname
  else:
       currency_name = None
  title='عدم الرد'
  context = {
  'title':title ,
  'Bookingfilter': Bookingfilter ,
  'web':weB,
  # count

  'count_notanswering':count_notanswering,

  }
  return render(request, 'waiting.html', context)

@login_required
#

def Appointment_confirmed(request):
    user = User.objects.get(id=request.user.id)
    weB = WEB.objects.filter(Employee_WEB=user).first()
    data = Appointment.objects.filter(web__Employee_WEB=user, status_appointment='confirmed')
    Bookingfilter = BookingFilter(request.GET, queryset=data)
    count_confirmed = data.count()
    # calendar
    now = dt.datetime.now()
    year = now.year
    month = now.month

    appointments = data.filter(date__year=year, date__month=month)
    month_name = now.strftime('%B')
    days = calendar.monthcalendar(year, month)

    # Count the number of appointments for each day
    counts = defaultdict(int)
    for appointment in appointments:
        counts[appointment.date.day] += 1
    if weB:
       currency_name = weB.currencyـname
    else:
       currency_name = None
    title = 'حجز مؤكد'
    context = {
        'title': title,
        'Bookingfilter': Bookingfilter,
        'web': weB,
        # count
        'count_confirmed':count_confirmed,
        # calendar
        'year': year,
        'month': month,
        'month_name': month_name,
        'today': now.day,
        'days': days,
        'appointments': appointments,
        'counts': counts,
    }

    return render(request, 'waiting000.html', context)



@login_required
def Appointment_visit(request):
  user = User.objects.get(id=request.user.id)
  weB = WEB.objects.filter(Employee_WEB=user).first()
  categories = Categories.objects.filter(web__Employee_WEB=user)
  services = Service.objects.filter(category_id__in=categories)
  booking = Appointment.objects.filter(web__Employee_WEB=user,status_appointment='visit')
  Bookingfilter = BookingFilter(request.GET, queryset=booking)


     # Count appointments by status
  count_visit = booking.count()
  title='حضر'
  if weB:
       currency_name = weB.currencyـname
  else:
       currency_name = None
  context = {
  'title':title ,
  'Bookingfilter': Bookingfilter ,
  'web':weB,

  # count

  'count_visit':count_visit,

  }
  return render(request, 'waiting.html', context)

@login_required
def Appointmentcancel (request):
  user = User.objects.get(id=request.user.id)
  weB = WEB.objects.filter(Employee_WEB=user).first()
  booking = Appointment.objects.filter(web__Employee_WEB=user,status_appointment='cancel')
  Bookingfilter = BookingFilter(request.GET, queryset=booking)

     # Count appointments by status
  count_cancel = booking.count()
  if weB:
         currency_name = weB.currencyـname
  else:
         currency_name = None

  title='إلغاءحجزه'
  context = {
  'title':title ,
  'Bookingfilter': Bookingfilter ,
  'web':weB,
  # count

  'count_cancel':count_cancel,


  }
  # return render(request, 'cancel.html', context)
  return render(request, 'waiting.html', context)



def Visitstoday(request):
    # Get the current user
    user = User.objects.get(id=request.user.id)
    sa_timezone = pytz.timezone('Asia/Riyadh')
    # Get the current date in the user's timezone
    # client_tz = timezone.get_current_timezone()  # or pytz.timezone(request.headers.get('timezone', 'UTC'))
    today = timezone.localtime(timezone.now(), sa_timezone).date()

    # confirmed_data = Appointment.objects.filter(
    #     web__Employee_WEB=user,
    #     status_appointment='confirmed',
    #     date=today,
    #     time__gte=timezone.localtime(timezone.now(), sa_timezone).time()
    # ).order_by('time')


    confirmed_data = Appointment.objects.filter(web__Employee_WEB=user, status_appointment='confirmed', date=today, time__gte=timezone.now().time()).order_by('time')

    count_visitstoday = confirmed_data.count()


    # Apply filters to the confirmed appointments
    Bookingfilter = BookingFilter(request.GET, queryset=confirmed_data)

    weB=WEB.objects.filter(Employee_WEB=user).first()
    if weB:
       currency_name = weB.currencyـname
    else:
       currency_name = None


    # Pass all data to the template
    title = ' الزيارات اليومية'
    context = {
        'count_visitstoday': count_visitstoday,
        'title': title,
        'Bookingfilter':Bookingfilter,
        'web':weB,
        'count_visitstoday':count_visitstoday
    }
    return render(request, 'waiting0.html', context)





def appointments_3_hours_ago(request):
    # Set the timezone to Arabia Standard Time (AST)
    sa_timezone = pytz.timezone('Asia/Riyadh')
    # Get the current time in Saudi Arabia


    sa_now = dt.datetime.now(sa_timezone)
    # Subtract 3 hours from the current time to get the time 3 hours ago
    sa_3_hours_ago = sa_now
    # Format the time as a string with am/pm
    sa_time_str = sa_3_hours_ago.strftime('%Y-%m-%d %I:%M %p')
    user = User.objects.get(id=request.user.id)
    weB = WEB.objects.filter(Employee_WEB=user)

    start_time = dt.datetime.strptime(sa_time_str, '%Y-%m-%d %I:%M %p')
    end_time= dt.datetime.strptime(sa_3_hours_ago.strftime('%Y-%m-%d %I:%M %p'), '%Y-%m-%d %I:%M %p')+ timedelta(hours=3)
    confirmed_data = Appointment.objects.filter(
    web__Employee_WEB=user,
    status_appointment='confirmed',
    date=sa_now.date(),
    # date=today,
    time__gte=start_time.time(),
    time__lte=end_time.time(),
    ).order_by('time')

    count_3_hours_ago=confirmed_data.count()


    Bookingfilter = BookingFilter(request.GET, queryset=confirmed_data)
    weB=WEB.objects.filter(Employee_WEB=user).first()
    if weB:
       currency_name = weB.currencyـname
    else:
       currency_name = None
    # Count appointments by status

    title = 'قبل 3 ساعات من الموعد'
    context = {
        'title': title,
        'Bookingfilter': Bookingfilter,
        'count_3_hours_ago':count_3_hours_ago,
         'web': weB
    }

    return render(request, 'waiting.html', context)



def appointments_1_hours_ago(request):
    # Set the timezone to Arabia Standard Time (AST)
    sa_timezone = pytz.timezone('Asia/Riyadh')
    # Get the current time in Saudi Arabia
    sa_now = dt.datetime.now(sa_timezone)
    # Subtract 3 hours from the current time to get the time 3 hours ago
    sa_3_hours_ago = sa_now
    # Format the time as a string with am/pm
    sa_time_str = sa_3_hours_ago.strftime('%Y-%m-%d %I:%M %p')
    user = User.objects.get(id=request.user.id)
    weB = WEB.objects.filter(Employee_WEB=user)

    start_time =dt.datetime.strptime(sa_time_str, '%Y-%m-%d %I:%M %p')
    end_time_1_hours_ago= dt.datetime.strptime(sa_3_hours_ago.strftime('%Y-%m-%d %I:%M %p'), '%Y-%m-%d %I:%M %p')+ timedelta(hours=1)
    confirmed_data1_1_hours_ago = Appointment.objects.filter(
    web__Employee_WEB=user,
    status_appointment='confirmed',
    date=sa_now.date(),
    # date=today,
    time__gte=start_time.time(),
    time__lte=end_time_1_hours_ago.time(),
    ).order_by('time')

    count_1_hours_ago=confirmed_data1_1_hours_ago.count()
    Bookingfilter = BookingFilter(request.GET, queryset=confirmed_data1_1_hours_ago)
    weB=WEB.objects.filter(Employee_WEB=user).first()
    if weB:
       currency_name = weB.currencyـname
    else:
       currency_name = None

    title =  'قبل ساعة من الموعد'
    context = {
        'title': title,
        'Bookingfilter': Bookingfilter,
        'count_1_hours_ago':count_1_hours_ago,
        'web': weB
    }

    return render(request, 'waiting.html', context)


def appointments_later(request):
    user = User.objects.get(id=request.user.id)
    weB = WEB.objects.filter(Employee_WEB=user)
    # Set the timezone to Arabia Standard Time (AST)
    sa_timezone = pytz.timezone('Asia/Riyadh')

    sa_now = dt.datetime.now(sa_timezone)
    # Get the start time of the day
    sa_start_of_day = sa_now.replace(hour=1, minute=0, second=0, microsecond=0)
    # Subtract 15 minutes from the current time
    sa_15_minutes_ago = sa_now - timedelta(minutes=15)
    # Format the time as a string with am/pm
    sa_time_str = sa_15_minutes_ago.strftime('%Y-%m-%d %I:%M %p')
    print('sa_time_str', sa_time_str)

    # Convert the string back to a datetime object
    sa_time = dt.datetime.strptime(sa_time_str, '%Y-%m-%d %I:%M %p')

    confirmed_data = Appointment.objects.filter(
        web__Employee_WEB=user,
        status_appointment='confirmed',
        date=sa_now.date(),
        time__gte=sa_start_of_day.time(),
        time__lte=sa_time.time(),
    ).order_by('time')

    count_appointments = confirmed_data.count()
    Bookingfilter = BookingFilter(request.GET, queryset=confirmed_data)

    title = 'حجز فائت تجاوز الموعد بـ15 دقيقة أو أكثر'
    weB=WEB.objects.filter(Employee_WEB=user).first()
    if weB:
       currency_name = weB.currencyـname
    else:
       currency_name = None
    context = {
        'title': title,
        'Bookingfilter': Bookingfilter,
        'count_appointments': count_appointments,
         'web': weB
    }

    return render(request, 'waiting.html', context)





def missedreservation(request):


    user = User.objects.get(id=request.user.id)
    weB = WEB.objects.filter(Employee_WEB=user)
    start_date = dt.datetime.min.date()
    end_date = dt.datetime.today().date() - timedelta(days=1)
    threshold_time = timezone.now() - timedelta(hours=3)
    appointments = Appointment.objects.filter(web__Employee_WEB=user,
        date__range=(start_date, end_date),
        status_appointment='confirmed')

    appointments.update(status_appointment='missed_reservation')
    missed_appointments = Appointment.objects.filter(
        date__range=(start_date, end_date),
        status_appointment='missed_reservation'
    )

    count_missed_appointments = missed_appointments.count()
    Bookingfilter = BookingFilter(request.GET, queryset=missed_appointments)
    title = 'حجز فائت'
  # count
    weB=WEB.objects.filter(Employee_WEB=user).first()
    if weB:
       currency_name = weB.currencyـname
    else:
       currency_name = None


    context = {
    'title':title ,
    'Bookingfilter': Bookingfilter ,
    'web':weB,
  # count
    'count_missed_appointments':count_missed_appointments,  }
    return render(request, 'waiting00.html', context)









@login_required
def update_status(request):

    appointment_id = request.GET.get('appointment_id')
    print('appointment_id', appointment_id)
    status = request.GET.get('status')
    print('status', status)
    appointment = Appointment.objects.get(id=appointment_id)
    print('appointment', appointment)
    appointment.status_appointment = status
    print('status_appointment', appointment)
    appointment.save()
    print('save', appointment)
    # Return a success response
    return JsonResponse({'success': True})

#  end  Appointment
# ===================================================



def NEW_appointment(request):
     try:

         web = WEB.objects.get(Employee_WEB=request.user)
         # Get all Categories objects for the current web object

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
             date = request.POST.get('id_date_' + str(service_id))
             time_str = request.POST.get('id_time_' + str(service_id))
             if time_str and date:
                 # Convert Arabic "pm" or "am" to English "pm" or "am"
                 time_str = time_str.replace('م', 'PM').replace('ص', 'AM')
                 # time = datetime.datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M:%S')
                 time = datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M:%S')
                 order.date = date
                 order.time = time
                 order.save()
                 print(time)
             else:
                 # Handle the case where the time string is empty
                 print('Time string is empty')



             order.service
             order.save()

             return redirect('Dashboard:Appointment_waiting')

     else:
         form = BookingForm()

      # Render the categories_services template with the category_services dictionary
     context={'category_services': category_services,'web': web,'form': form}
     # Render the categories_services template with the category_services dictionary
     return render(request, 'add.html', context)

from decimal import Decimal
import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404





def add_to_appointment(request, pk, web_slug):
    print('ok')
    web = get_object_or_404(WEB, slug=web_slug)
    if request.method == 'GET':
        service = get_object_or_404(Service, id=pk, web=web)
        doctor = service.doctors
        schedules = DoctorSchedule.objects.filter(doctor=doctor)
        current_date = datetime.date.today()
        ten_days_from_now = current_date + datetime.timedelta(days=10)
        schedules = schedules.filter(date__range=[current_date, ten_days_from_now])
        dates = [schedule.date.strftime('%Y-%m-%d') for schedule in schedules]
        print('dates',dates)
        response_data = {
            'serviceId': pk,
            'webSlug': web_slug,
            'dates': dates
        }
        return JsonResponse(response_data)
    elif request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        service_id = data.get('serviceId')
        web_slug = data.get('webSlug')
        date_str = data.get('date')
        print('date_str',date_str)
        service = get_object_or_404(Service, id=service_id, web=web)
        doctor = service.doctors
        schedules = DoctorSchedule.objects.filter(doctor=doctor, web=web)

        if date_str:
            try:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                schedule = schedules.filter(date=date, doctor=doctor).first()
                print('schedule', schedule)

                appointment = Appointment.objects.filter(date=date, service=service, web=web)
                appointment_times = set(appointment.values_list('time', flat=True))
                available_times1 = []
                available_times2 = []
                timetaken = Decimal(doctor.timetaken)

                first_period_start = schedule.first_period_start
                # print('first_period_start', first_period_start)
                first_period_end = schedule.first_period_end
                # print('first_period_end', first_period_end)
                second_period_start = schedule.second_period_start
                # print('second_period_start', second_period_start)
                second_period_end = schedule.second_period_end
                # print('second_period_end', second_period_end)

                timetaken = doctor.timetaken
                Timetaken = timetaken + doctor.WaitTime
                increment = datetime.timedelta(minutes=int(Timetaken))

                current_time1 = datetime.datetime.combine(date, first_period_start)

                while current_time1.time() <= first_period_end:
                    if current_time1.time() not in appointment_times and current_time1.time() not in available_times1:
                        available_times1.append(current_time1.time())
                    current_time1 += increment

                print(current_time1)

                available_times = available_times1

                current_time2 = None
                if second_period_start:
                    current_time2 = datetime.datetime.combine(date, second_period_start)

                if current_time2 is not None:
                    while current_time2.time() <= second_period_end:
                        if current_time2.time() not in appointment_times and current_time2.time() not in available_times2:
                            available_times2.append(current_time2.time())
                        current_time2 += increment

                    available_times += available_times2

                response_times = [time.strftime('%I:%M %p').replace('AM', 'ص').replace('PM', 'م') for time in available_times]

                return JsonResponse({'success': True, 'available_times': response_times})

            except ValueError:
                return JsonResponse({'success': False, 'message': 'Invalid date format'})
        else:
            return JsonResponse({'success': False, 'message': 'Date is required'})
