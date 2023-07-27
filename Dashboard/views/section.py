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
def create_section(request ):
    if request.method == 'POST':
        form = SectionForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new Section object and save it
            section = form.save(commit=False)
            web = WEB.objects.filter(Employee_WEB=request.user).first()
            section.web = web
            section.save()
            return redirect('Dashboard:dashboard')
    else:
        form = SectionForm()
    title=' إضافة خدمات'
    context = {'form': form, 'title':title }
    return render(request, 'create_section.html', context)


@login_required
def update_section(request, section_id):
    # Get the section object with the given id
    section = get_object_or_404(Section, id=section_id)

    if request.method == 'POST':
        # Create a form instance with the submitted data and the section object as the instance to update
        form = SectionForm(request.POST, request.FILES, instance=section)

        if form.is_valid():
            # Save the updated Doctor object
            form.save()
            return redirect('Dashboard:dashboard')
    else:
        # Create a form instance with the section object to pre-fill the form
        form = SectionForm(instance=section)

    # Render the updatesection page with the form and doctor object
    title='  تحديث الخدمة '
    context = {'form': form, 'title':title ,'section':section}
    return render(request, 'update_section.html', context)



@login_required
def delete_section(request, id):
    section = Section.objects.get(id=id)
    if request.method == 'POST':
        section.delete()
        return redirect('Dashboard:dashboard')

    context = {'section': section}
    return render(request, 'delete_service.html', context)


#  end section
