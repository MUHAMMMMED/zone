import os
# Create your views here.
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
from datetime import date, datetime, timedelta
import calendar
from collections import defaultdict
from django.db.models import Q
from django.db.models import Count
from django.db.models import F
from django.utils import timezone
from django.conf import settings
from django.db.models.functions import StrIndex
from calendar import monthrange
import json
import pytz
#
from webs.models import *
from Dashboard.forms import *
from webs.form import *
from Dashboard.filters import *


@login_required
def dashboard(request):
    user = User.objects.get(id=request.user.id)
    weB = WEB.objects.filter(Employee_WEB=user).first()


    settings_password = weB.settings_password
    REPORT_password = weB.Report_password
    settings_appointment =weB.Appointment_password

    if request.method == 'POST':
        password1=  request.POST.get('settings')
        password2 = request.POST.get('REPORT')
        password3 = request.POST.get('bookingsupport')

        if password1 == settings_password:
            # randomcode = generate_random_code()
            return redirect('Dashboard:Settings', )

        elif password2 == REPORT_password:
            # randomcode = generate_random_code()
            return redirect('Dashboard:Report', )

        elif password3 == settings_appointment:
            return redirect('Dashboard:Appointment_waiting')

    return render(request, 'welcomDash.html')
 
@login_required
def Settings(request):
    user = User.objects.get(id=request.user.id)
    weB = WEB.objects.filter(Employee_WEB=user)
    links = Link.objects.filter(web__in=weB)
    print('links',links)
    categories = Categories.objects.filter(web__Employee_WEB=user)
    doctors = Doctors.objects.filter(web__in=weB)
    department=Department.objects.filter(web__in=weB)
    section = Section.objects.filter(web__in=weB)
    insurance = Insurance.objects.filter(web__in=weB)
    image= Image.objects.filter(web__in=weB)
    questions=Questions.objects.filter(web__in=weB)
    count = Appointment.objects.filter(web__Employee_WEB=user, status_appointment='انتظار').count()
        # Retrieve the Service objects that belong to the specific Categories object(s)
    services = Service.objects.filter(category_id__in=categories)
    context = {
        'count': count ,
        'weB': weB,
        'user': user,
        'links':links,
        'categories': categories,
        'services': services,
        'Section':section,
        'doctors':doctors,
        'Insurance':insurance,
        'Image':image,
        'Questions':questions,
        'department':department,
    }
    return render(request, 'dashboard.html', context)



@login_required
def create_web(request):
    if not request.user.is_employee():
        return redirect('Dashboard:display_bookings')  # or any other URL you want
    if request.method == 'POST':
        form = WebForm(request.POST, request.FILES )
        if form.is_valid():
            web = form.save(commit=False)
        if form.is_valid():
            web = form.save(commit=False)
            user = User.objects.get(id=request.user.id)
            web.Employee_WEB=user
            web.save()
            return redirect('Dashboard:dashboard')
    else:
        form = WebForm()
    return render(request, 'web_form.html', {'form': form})

@login_required
def update_web(request, pk):
    # Retrieve the object you want to update
    web = get_object_or_404(WEB, pk=pk)
    if request.method == 'POST':
        # Create a form instance with the updated data
        form = WebFormUP(request.POST, request.FILES, instance=web)
        if form.is_valid():
            # Save the changes to the database
            form.save()
            return redirect('Dashboard:dashboard')
    else:
        # Create a form instance with the current data
        form = WebFormUP(instance=web)
    return render(request, 'web_form.html', {'form': form})


@login_required
def update_web_admin(request, pk):
    # Retrieve the object you want to update
    web = get_object_or_404(WEB, pk=pk)
    if request.method == 'POST':
        # Create a form instance with the updated data
        form = WebForm(request.POST, request.FILES, instance=web)
        if form.is_valid():
            # Save the changes to the database
            form.save()
            return redirect('Users:manager_dashboard')
    else:
        # Create a form instance with the current data
        form = WebForm(instance=web)
    return render(request, 'web_form.html', {'form': form})
