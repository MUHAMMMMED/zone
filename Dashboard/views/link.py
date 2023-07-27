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


def create_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            # Create a new Link object with the form data, related to the current user's WEB object
            web = WEB.objects.filter(Employee_WEB=request.user).first()
            link = form.save(commit=False)
            link.web = web
            link.save()
            # Redirect to a success page
            return redirect('Dashboard:dashboard')
    else:
        form = LinkForm()
    return render(request, 'create_or_update_link.html', {'form': form})



def update_link(request, pk):
    # Get the Link object
    link = get_object_or_404(Link, id=pk)
    if request.method == 'POST':
        # Populate the form with the POST data and the Link object
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            # Save the updated form data
            link = form.save()
            # Redirect to a success page
            return redirect('Dashboard:dashboard')
    else:
        # Populate the form with the Link object
        form = LinkForm(instance=link)
    return render(request, 'create_or_update_link.html', {'form': form})
