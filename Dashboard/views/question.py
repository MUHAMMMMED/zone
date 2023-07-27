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



#  start question
@login_required
def create_question(request ):
    # Get the WEB object with the given slug
    if request.method == 'POST':
        form = QuestionsForm(request.POST)

        if form.is_valid():
            # Create a new Questions object and save it
            question = form.save(commit=False)
            web = WEB.objects.filter(Employee_WEB=request.user).first()
            question.web = web
            question.save()

            return redirect('Dashboard:dashboard')
    else:
        form = QuestionsForm()
    title='   اضافة سؤال جديد '
    context = {'form': form, 'title':title }
    return render(request, 'create_question.html', context)

@login_required
def update_question(request, question_id):

    question = get_object_or_404(Questions, id=question_id)
    if request.method == 'POST':
        form = QuestionsForm(request.POST, instance=question)
        if form.is_valid():
            image = form.save()
            return redirect('Dashboard:dashboard')
    else:
        form = QuestionsForm(instance= question)

    title='   تحديث السؤال        '
    context = {'form': form, 'title':title ,'question': question}
    return render(request, 'create_question.html', context)



@login_required
def delete_question(request, id):
    question = Questions.objects.get(id=id)
    if request.method == 'POST':
        question.delete()
        return redirect('Dashboard:dashboard')

    context = {'question': question}
    return render(request, 'delete_service.html', context)



#  end question
