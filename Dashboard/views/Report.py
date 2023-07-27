# import os
# # Create your views here.
# from django.shortcuts import render, get_object_or_404, redirect
# from django.urls import reverse
# from django.views.decorators.http import require_http_methods
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.db.models import Sum
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
# from django.views.decorators.csrf import csrf_exempt
# from django.db import IntegrityError
# from datetime import date, datetime, timedelta
# import calendar
# from collections import defaultdict
# from django.db.models import Q
# from django.db.models import Count
# from django.db.models import F
# from django.utils import timezone
# from django.conf import settings
# from django.db.models.functions import StrIndex
# from calendar import monthrange
# import json
# import pytz
# #
# from webs.models import *
# from Dashboard.forms import *
# from webs.form import *
# from Dashboard.filters import *
#
#
# from datetime import datetime, timedelta
#
# from django.db.models import Sum, Q
#
# @login_required
# def Report(request):
#
#     user = User.objects.get(id=request.user.id)
#     weB = WEB.objects.filter(Employee_WEB=user)
#     web = weB.first()
#
#     end_date = datetime.now().date() # Define end_date here
#     # Define the default date ranges
#     last_week = end_date - timedelta(days=7)
#     last_month = end_date - timedelta(days=30)
#
#     if request.method == 'POST':
#        start_date = request.POST.get('start_date')
#        end_date = request.POST.get('end_date')
#     else:
#     # If no dates are provided, use the last month as the default date range
#          start_date = last_week
#          end_date = end_date # Use the previously defined end_date
#
#     appointment = Appointment.objects.filter(web__Employee_WEB=user,  date__range=[start_date, end_date])
#     appointments = Appointment.objects.filter(web__Employee_WEB=user  )
#
#
#     CountـPatient = Patient.objects.filter(web__Employee_WEB=user).count()
#
#
#
#
#
#
#     ClientStatus_New = appointments.filter(ClientStatus='جديد').count()
#     ClientStatus_Old = appointments.filter(ClientStatus='قديم').count()
#     ClientStatus_Undefined = appointments.filter(ClientStatus='غير محدد').count()
#
#     knew_from = appointments.values('knew_from').annotate(count=Count('knew_from')).order_by('-count')
#
#     count_inquiries = appointments.filter(status_appointment='inquiries').count()
#     count_waiting = appointments.filter( status_appointment='انتظار').count()
#     count_notanswering = appointments.filter( status_appointment='notanswering').count()
#     count_confirmed = appointments.filter(status_appointment='confirmed').count()
#     count_visit = appointments.filter( status_appointment='visit') .count()
#     count_cancel = appointments.filter( status_appointment='cancel').count()
#     count_missed_reservation = appointments.filter( status_appointment='missed_reservation').count()
#
#     price_by_status = appointments.values('status_appointment').annotate(total_price=Sum('price')).order_by('status_appointment', '-total_price')
#
#
#
#     Appoin = appointments.filter(Q(status_appointment='cancel') | Q(status_appointment='confirmed') | Q(status_appointment='انتظار') | Q(status_appointment='notanswering') | Q(status_appointment='inquiries'))
# # Get the total price for all appointments with serviceName
#     service_price_query = Appoin.values('serviceName').annotate(total_price=Sum('price')).order_by('-total_price')
#     service_price = {item['serviceName']: item['total_price'] for item in service_price_query}
#
#     count_price = appointments.aggregate(Sum('price'))['price__sum']
#     formatted_count_price_visit = appointments.filter(status_appointment='visit').aggregate(Sum('price'))['price__sum'] or 0
#     count_price_visit = "{:.2f}".format(formatted_count_price_visit)
#     missing =[0]
#     if count_price is not None and count_price_visit is not None:
#          missing = count_price - count_price_visit
#     else:
#         missing = None
#     if count_price and count_price_visit:
#        percentageformatted_percentage = (count_price_visit / count_price) * 100
#        percentage = "{:.2f}%".format(percentageformatted_percentage)
#     else:
#        percentage = None
import os
from decimal import Decimal
from datetime import date, datetime, timedelta, time
import calendar
from collections import defaultdict
import json
import pytz
from calendar import monthrange

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.db.models import Count, F, Q, Sum
from django.db.models.functions import StrIndex
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from webs.models import WEB, Patient, Appointment, User
from Dashboard.filters import *
from Dashboard.forms import *
from webs.form import *


@login_required
def Report(request):

    user = User.objects.get(id=request.user.id)
    weB = WEB.objects.filter(Employee_WEB=user)
    web = weB.first()

    end_date = datetime.now().date() # Define end_date here
    # Define the default date ranges
    last_week = end_date - timedelta(days=7)
    last_month = end_date - timedelta(days=30)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
    else:
        # If no dates are provided, use the last month as the default date range
        start_date = last_week
        end_date = end_date # Use the previously defined end_date

    appointment = Appointment.objects.filter(web__Employee_WEB=user,  date__range=[start_date, end_date])
    appointments = Appointment.objects.filter(web__Employee_WEB=user)

    CountـPatient = Patient.objects.filter(web__Employee_WEB=user).count()

    ClientStatus_New = appointments.filter(ClientStatus='جديد').count()
    ClientStatus_Old = appointments.filter(ClientStatus='قديم').count()
    ClientStatus_Undefined = appointments.filter(ClientStatus='غير محدد').count()

    knew_from = appointments.values('knew_from').annotate(count=Count('knew_from')).order_by('-count')

    count_inquiries = appointments.filter(status_appointment='inquiries').count()
    count_waiting = appointments.filter(status_appointment='انتظار').count()
    count_notanswering = appointments.filter(status_appointment='notanswering').count()
    count_confirmed = appointments.filter(status_appointment='confirmed').count()
    count_visit = appointments.filter(status_appointment='visit').count()
    count_cancel = appointments.filter(status_appointment='cancel').count()
    count_missed_reservation = appointments.filter(status_appointment='missed_reservation').count()

    price_by_status = appointments.values('status_appointment').annotate(total_price=Sum('price')).order_by('status_appointment', '-total_price')

    Appoin = appointments.filter(Q(status_appointment='cancel') | Q(status_appointment='confirmed') | Q(status_appointment='انتظار') | Q(status_appointment='notanswering') | Q(status_appointment='inquiries'))
    # Get the total price for all appointments with serviceName
    service_price_query = Appoin.values('serviceName').annotate(total_price=Sum('price')).order_by('-total_price')
    service_price = {item['serviceName']: item['total_price'] for item in service_price_query}

    count_price = appointments.aggregate(Sum('price'))['price__sum']
    formatted_count_price_visit = appointments.filter(status_appointment='visit').aggregate(Sum('price'))['price__sum'] or 0
    count_price_visit = Decimal("{:.2f}".format(formatted_count_price_visit))
    missing = Decimal(0)
    if count_price is not None and count_price_visit is not None:
        missing = count_price - count_price_visit
    else:
        missing = None
    if count_price and count_price_visit:
        percentageformatted_percentage = (count_price_visit / count_price) * 100
        percentage = "{:.2f}%".format(percentageformatted_percentage)
    else:
        percentage = None


    missing = float(missing)
# ??????
    Doctor = Doctors_pixel.objects.filter(web__Employee_WEB=user,  date__range=[start_date, end_date])
    category = Categories_pixel.objects.filter(web__Employee_WEB=user,  date__range=[start_date, end_date])
    Service= Service_pixel.objects.filter(web__Employee_WEB=user,  date__range=[start_date, end_date])
    pixel_all = pixel.objects.filter(web__Employee_WEB=user,  date__range=[start_date, end_date])

    Doctors_total_views = Doctor.aggregate(Sum('views'))['views__sum']
    Doctors_total_booking = Doctor.aggregate(Sum('booking'))['booking__sum']
    Doctors_total_click_whatsapp = Doctor.aggregate(Sum('click_whatsapp'))['click_whatsapp__sum']

    categories_total_views = category.aggregate(Sum('views'))['views__sum']
    categories_total_booking = category.aggregate(Sum('booking'))['booking__sum']
    categories_total_click_whatsapp  = category.aggregate(Sum('click_whatsapp'))['click_whatsapp__sum']

    Service_total_views = Service.aggregate(Sum('views'))['views__sum']
    Service_total_booking = Service.aggregate(Sum('booking'))['booking__sum']
    Service_total_click_whatsapp  = Service.aggregate(Sum('click_whatsapp'))['click_whatsapp__sum']

    views_Home_count = pixel_all.aggregate(Sum('views_Home'))['views_Home__sum']
    click_whatsapp_Home_count = pixel_all.aggregate(Sum('click_whatsapp_Home'))['click_whatsapp_Home__sum']
    views_Allcategories_count = pixel_all.aggregate(Sum('views_Allcategories'))['views_Allcategories__sum']
    click_whatsapp_Allcategories_count = pixel_all.aggregate(Sum('click_whatsapp_Allcategories'))['click_whatsapp_Allcategories__sum']
    views_Confirmation_count = pixel_all.aggregate(Sum('views_Confirmation'))['views_Confirmation__sum']
    click_whatsapp_Doctor_count = pixel_all.aggregate(Sum('click_whatsapp_Doctor'))['click_whatsapp_Doctor__sum']
    view_Doctor_count = pixel_all.aggregate(Sum('view_Doctor'))['view_Doctor__sum']
    views_Link_page_count =pixel_all.aggregate(Sum('views_Link_page'))['views_Link_page__sum']

    # Total_views=Doctors_total_views+categories_total_views+Service_total_views+views_Home_count+views_Allcategories_count+views_Confirmation_count+

    Total_views = 0
    if Doctors_total_views is not None:
        Total_views += Doctors_total_views
    if categories_total_views is not None:
        Total_views += categories_total_views
    if Service_total_views is not None:
        Total_views += Service_total_views
    if views_Home_count is not None:
        Total_views += views_Home_count
    if views_Allcategories_count is not None:
        Total_views += views_Allcategories_count
    if views_Confirmation_count is not None:
        Total_views += views_Confirmation_count
    if views_Link_page_count is not None:
        Total_views += views_Link_page_count

    Total_booking= Service_total_booking

    Total_click_whatsapp = 0
    if Service_total_click_whatsapp is not None:
        Total_click_whatsapp += Service_total_click_whatsapp
    if categories_total_click_whatsapp is not None:
        Total_click_whatsapp += categories_total_click_whatsapp
    if Doctors_total_click_whatsapp is not None:
        Total_click_whatsapp += Doctors_total_click_whatsapp
    if click_whatsapp_Home_count is not None:
        Total_click_whatsapp += click_whatsapp_Home_count
    if click_whatsapp_Doctor_count is not None:
        Total_click_whatsapp += click_whatsapp_Doctor_count

    services = Service_pixel.objects.filter(web=web, date__range=[start_date, end_date])
    service_stats = []
    for service in services:
        service_stat = {}
        service_stat['name'] = service.ServiceName
        service_stat['views'] = service.views
        service_stat['click_whatsapp'] = service.click_whatsapp
        service_stat['booking'] = service.booking
        service_stats.append(service_stat)
        service_stats = sorted(service_stats, key=lambda x: x['booking'], reverse=True)

    categories = Categories_pixel.objects.filter(web=web, date__range=[start_date, end_date])
    categories_stats = []
    for category in categories:
       category_stat = {}
       category_stat['name'] = category.CategoryName
       category_stat['views'] = category.views
       category_stat['click_whatsapp'] = category.click_whatsapp
       category_stat['booking'] = category.booking
       categories_stats.append(category_stat)
       categories_stats = sorted(categories_stats, key=lambda x: x['booking'], reverse=True)

    doctors = Doctors_pixel.objects.filter(web=web, date__range=[start_date, end_date])
    doctor_stats = []
    for doctor in doctors:
        doctor_stat = {}
        doctor_stat['name'] = doctor.DoctorName
        doctor_stat['views'] = doctor.views
        doctor_stat['click_whatsapp'] = doctor.click_whatsapp
        doctor_stat['booking'] = doctor.booking
        doctor_stats.append(doctor_stat)
        doctor_stats = sorted(doctor_stats, key=lambda x: x['booking'], reverse=True)

    pixel_data = pixel.objects.filter(web=web, date__range=[start_date, end_date])
    pixel_stats = pixel_data.aggregate(
          Sum('views_Home'), Sum('click_whatsapp_Home'),
          Sum('views_Allcategories'), Sum('click_whatsapp_Allcategories'),
          Sum('views_Confirmation'), Sum('click_whatsapp_Doctor'),
          Sum('view_Doctor'), Sum('views_Link_page'))

    context = {
        'web': weB,
        'user': user,
        # count
        'count_waiting': count_waiting,
        'count_inquiries': count_inquiries,
        'count_notanswering': count_notanswering,
        'count_confirmed': count_confirmed,
        'count_visit': count_visit,
        'count_cancel': count_cancel,
        'count_missed_reservation':count_missed_reservation,
        'CountـPatient':CountـPatient,
        'ClientStatus_New': ClientStatus_New,
        'ClientStatus_Old': ClientStatus_Old,
        'ClientStatus_Undefined': ClientStatus_Undefined,
#
        'doctor_stats': doctor_stats,
        'service_stats': service_stats,
        'categories_stats':categories_stats,
        'pixel_stats': pixel_stats,
#
        'knew_from': knew_from,
        'Total_views':Total_views,
        'Total_click_whatsapp':Total_click_whatsapp ,
        'Total_booking':Total_booking ,
        'count_price':count_price,
        'count_price_visit':count_price_visit,
        'missing':missing,
        'percentage':percentage,

        'service_price': service_price,
        'price_by_status':price_by_status
    }
    return render(request, 'report.html', context)
