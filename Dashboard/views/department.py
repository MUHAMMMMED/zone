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

 #  start department
@login_required
def create_department(request):
    # Get the WEB object with the given slug
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            # Create a new Department object and save it
            department = form.save(commit=False)
            web = WEB.objects.filter(Employee_WEB=request.user).first()
            department.web = web
            department.save()
            return redirect('Dashboard:dashboard')
    else:
        form = DepartmentForm()
    title=' إضافة قسم '
    context = {'form': form, 'title':title }
    return render(request, 'create_department.html', context)

@login_required
def update_department(request,  department_id):

    department = get_object_or_404(Department, id=department_id)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)

        if form.is_valid():

            form.save()
            return redirect('Dashboard:dashboard')
    else:
        form = DepartmentForm(instance=department)

    title='  تحديث القسم '
    context = {'form': form, 'title':title ,'department':department}
    return render(request, 'create_department.html', context)




@login_required
def delete_department(request, id):
    department = Department.objects.get(id=id)
    if request.method == 'POST':
        department.delete()
        return redirect('Dashboard:dashboard')

    context = {'department': department}
    return render(request, 'delete_service.html', context)

#  end department
