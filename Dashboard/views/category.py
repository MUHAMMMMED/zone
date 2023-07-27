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



#  end question


#  start category
@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoriesForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            web = WEB.objects.filter(Employee_WEB=request.user).first()
            if web is None:
                # handle the case where no web instance is found for the current user
                pass
            else:
                category.web = web
                category.save()
                return redirect('Dashboard:dashboard')
    else:
        form = CategoriesForm()
    title='   اضافة تصنيف جديد        '
    context = {'form': form, 'title':title }
    return render(request, 'create_category.html',context)


@login_required
def update_category(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    if request.method == 'POST':
        form = CategoriesForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            if 'Image' in request.FILES:
                # Delete the previous image file if it exists
                if os.path.exists(category.Image.path):
                    os.remove(category.Image.path)
            category = form.save(commit=False)
            web = WEB.objects.filter(Employee_WEB=request.user).first()
            if web is None:
                # handle the case where no web instance is found for the current user
                pass
            else:
                category.web = web
                category.save()
                return redirect('Dashboard:dashboard')

    else:
        form = CategoriesForm(instance=category)
    title='   تحديث التصنيف        '
    context = {'form': form, 'title':title,'category':category }
    return render(request, 'update_category.html',context)



@login_required
def delete_category(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    if request.method == 'POST':
        # Delete the image file if it exists
        if category.Image:
            category.Image.delete()
        category.delete()
        return redirect('Dashboard:dashboard')

    context = {'category': category}
    return render(request, 'delete_category.html', context)

#  end category
