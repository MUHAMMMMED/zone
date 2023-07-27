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


#  start insurance
@login_required
def create_insurance(request  ):
    # Get the WEB object with the given slug
    if request.method == 'POST':
        form = InsuranceForm(request.POST)

        if form.is_valid():
            # Create a new Insurance object and save it
            insurance = form.save(commit=False)
            web = WEB.objects.filter(Employee_WEB=request.user).first()
            insurance.web = web
            insurance.save()
            return redirect('Dashboard:dashboard')
    else:
        form = InsuranceForm()
    title='  إضافة تأمين    '
    context = {'form': form, 'title':title }
    return render(request, 'create_insurance.html', context)


@login_required
def update_insurance(request, insurance_id):

    insurance = get_object_or_404(Insurance, id=insurance_id)

    if request.method == 'POST':
        form = InsuranceForm(request.POST, instance=insurance)

        if form.is_valid():

            form.save()
            return redirect('Dashboard:dashboard')
    else:
        form = InsuranceForm(instance=insurance)

    title=' تحديث  التأمين '
    context = {'form': form, 'title':title ,'insurance':insurance}
    return render(request, 'create_insurance.html', context)


@login_required
def delete_insurance(request, id):
    insurance = Insurance.objects.get(id=id)
    if request.method == 'POST':
        insurance.delete()
        return redirect('Dashboard:dashboard')

    context = {'insurance': insurance}
    return render(request, 'delete_service.html', context)
#  end insurance
 
