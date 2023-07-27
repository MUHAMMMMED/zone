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

#  start image
@login_required
def create_image(request ):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new Image object and save it
            image = form.save(commit=False)
            web = WEB.objects.filter(Employee_WEB=request.user).first()
            image.web = web
            image.save()
            return redirect('Dashboard:dashboard')
    else:
        form = ImageForm()
    title='إضافة صوره'
    context = {'form': form, 'title':title}
    return render(request, 'create_image.html', context)

@login_required
def update_image(request, image_id):

    image = get_object_or_404(Image, id=image_id)
    if request.method == 'POST':
        form = ImageForm(request.POST, instance=image)
        if form.is_valid():
            form.save()
            return redirect('Dashboard:dashboard')
    else:
        form = ImageForm(instance=image)

    title=' تحديث  الصورة  '
    context = {'form': form, 'title':title ,'image': image}
    return render(request, 'update_image.html', context)


@login_required
def delete_image(request, id):
    image = Image.objects.get(id=id)
    if request.method == 'POST':
        image.delete()
        return redirect('Dashboard:dashboard')

    context = {'image': image}
    return render(request, 'delete_service.html', context)

#  end image


 
