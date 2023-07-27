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

 #  start  Appointment

# def Patient_profile(request, id):
#     user = User.objects.get(id=request.user.id)
#     web = WEB.objects.get(Employee_WEB=user)
#     patient = get_object_or_404(Patient, id=id)
#     # patient = patient.objects.filter(web=web)
#
#     appointments = Appointment.objects.filter(patient=patient, web=web)
#     countAppointment = appointments.count()
#     most_recent_appointment = Appointment.objects.order_by('-created_at').first()
#
#     total_price = appointments.aggregate(total_cost=Sum('price'))['patient '] or 0
#
#     # Get the created_at timestamp of the most recent appointment
#     last_created_at = most_recent_appointment.created_at if most_recent_appointment else None
#
#     context = {
#         'patient': patient,
#         'appointments': appointments,
#         'last_created_at': last_created_at,
#         # 'total_cost': total_cost,
#         'countAppointment': countAppointment,
#
#     }
#     return render(request, 'Patientprofile.html', context)
#

from django.db.models import Sum

# def Patient_profile(request, id):
#     user = User.objects.get(id=request.user.id)
#     web = WEB.objects.get(Employee_WEB=user)
#     patient = get_object_or_404(Patient, id=id)
#
#     appointments = Appointment.objects.filter(patient=patient, web=web)
#     countAppointment = appointments.count()
#     most_recent_appointment = Appointment.objects.order_by('-created_at').first()
#
#     # Calculate the total price of all appointments for the patient
#     num= appointments.aggregate(total_cost=Sum('price'))['total_cost'] or 0
#
#     total_price.format(num)
#
#     # Get the created_at timestamp of the most recent appointment
#     last_created_at = most_recent_appointment.created_at if most_recent_appointment else None
#
#     context = {
#         'patient': patient,
#         'appointments': appointments,
#         'last_created_at': last_created_at,
#         'total_price': total_price,
#         'countAppointment': countAppointment,
#     }
#     return render(request, 'Patientprofile.html', context)
# def Patient_profile(request, id):
#     user = User.objects.get(id=request.user.id)
#     web = WEB.objects.get(Employee_WEB=user)
#     patient = get_object_or_404(Patient, id=id)
#
#     appointments = Appointment.objects.filter(patient=patient, web=web)
#     countAppointment = appointments.count()
#     most_recent_appointment = Appointment.objects.order_by('-created_at').first()
#
#     # Calculate the total price of all appointments for the patient
#     total_price = appointments.aggregate(total_cost=Sum('price'))['total_cost'] or 0
#
#     # Format the total_price variable with two decimal places
#     formatted_total_price = "{:.2f}".format(total_price)
#
#     # Pass the formatted total_price variable to the template
#     context = {
#         'patient': patient,
#         'appointments': appointments,
#         'last_created_at': most_recent_appointment.created_at if most_recent_appointment else None,
#         'total_price': formatted_total_price,
#         'countAppointment': countAppointment,
#     }
    #
    # return render(request, 'Patientprofile.html', context)


def Patient_profile(request, id):
    user = User.objects.get(id=request.user.id)
    web = WEB.objects.get(Employee_WEB=user)
    patient = get_object_or_404(Patient, id=id)

    appointments = Appointment.objects.filter(patient=patient, web=web)
    booking = Appointment.objects.filter(web=web,patient=patient, status_appointment='visit')


    countAppointment = appointments.count()

    # Get all appointments in descending order of created_at
    ordered_appointments = Appointment.objects.filter(patient=patient, web=web).order_by('-created_at')

    # Get the second most recent appointment
    second_most_recent_appointment = ordered_appointments[1] if len(ordered_appointments) > 1 else None

    # Calculate the total price of all appointments for the patient
    total_price = booking.aggregate(total_cost=Sum('price'))['total_cost'] or 0

#
#     # Format the total_price variable with two decimal places
    formatted_total_price = "{:.2f}".format(total_price)
    context = {
        'patient': patient,
        'appointments': appointments,
        'last_created_at': second_most_recent_appointment.created_at if second_most_recent_appointment else None,
        'total_price': formatted_total_price,
        'countAppointment': countAppointment,
    }
    return render(request, 'Patientprofile.html', context)



















def update_patient(request, patient_id):
    # Get the patient object with the given ID
    user = User.objects.get(id=request.user.id)
    weB = WEB.objects.filter(Employee_WEB=user)
    patient = get_object_or_404(Patient, id=patient_id,web__Employee_WEB=user)

    # Populate the form with the patient's existing data
    form = PatientForm(instance=patient)

    # Handle form submission
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('Dashboard:Patientprofile', id=patient_id)

    context = {
        'form': form,
        'patient': patient,
    }
    return render(request, 'update_patient.html', context)
