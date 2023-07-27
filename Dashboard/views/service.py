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

 #  start service

@login_required

def create_service(request):
    user = User.objects.get(id=request.user.id)
    weB = WEB.objects.filter(Employee_WEB=user)
    categories = Categories.objects.filter(web__Employee_WEB=user)
    doctors = Doctors.objects.filter(web__Employee_WEB=user)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)

            web = WEB.objects.filter(Employee_WEB=request.user).first()
            service.web = web
            category_id = request.POST.get('category_id')
            if category_id:
                category = Categories.objects.get(id=category_id)
            else:
                category = None
            service.category_id = category

            doctor_id = request.POST.get('id_doctor')
            if doctor_id:
                doctor = Doctors.objects.get(id=doctor_id)
                service.doctors = doctor

            service.save()
            return redirect('Dashboard:dashboard')
    else:
        form = ServiceForm(initial={'category_id': categories.first()})

    title = 'إضافة عرض جديد'
    context = {'form': form, 'title': title, 'categories': categories, 'doctors': doctors}
    return render(request, 'create_service.html', context)

# @login_required
def update_service(request, service_id):
    user = User.objects.get(id=request.user.id)
    weB = WEB.objects.filter(Employee_WEB=user)
    categories = Categories.objects.filter(web__Employee_WEB=user)
    doctors = Doctors.objects.filter(web__Employee_WEB=user)

    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)

        if form.is_valid():
            service = form.save(commit=False)
            web = WEB.objects.filter(Employee_WEB=request.user).first()

            service.web = web
            category_id = request.POST.get('category_id')
            if category_id:
                category = Categories.objects.get(id=category_id)
                service.category_id = category

            doctor_id = request.POST.get('id_doctor')
            if doctor_id:
                doctor = Doctors.objects.get(id=doctor_id)
                service.doctors = doctor

            service.save()
            return redirect('Dashboard:dashboard')

    else:
        form = ServiceForm(instance=service, initial={'category_id': service.category_id})

    title = 'تحديث العرض'
    context = {'form': form, 'title': title, 'service': service, 'categories': categories, 'doctors': doctors}
    return render(request, 'update_service.html', context)



# @login_require

def Service_delete(request, id):
    service = Service.objects.get(id=id)

    if request.method == 'POST':
        service.delete()
        return redirect('Dashboard:dashboard')

    context = {'service': service}
    return render(request, 'delete_service.html', context)


#  end service


#  start  Appointment
