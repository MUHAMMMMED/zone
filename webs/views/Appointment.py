
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime
import json
from decimal import Decimal
from webs.models import *
from Dashboard.forms import *
from webs.form import *
from Dashboard.filters import *


from decimal import Decimal
#
# def add_to_appointment(request, pk, web_slug):
#     web = get_object_or_404(WEB, slug=web_slug)
#     if request.method == 'GET':
#         service = get_object_or_404(Service, id=pk, web=web)
#         doctor = service.doctors
#         schedules = DoctorSchedule.objects.filter(doctor=doctor)
#         current_date = datetime.date.today()
#         ten_days_from_now = current_date + datetime.timedelta(days=10)
#         schedules = schedules.filter(date__range=[current_date, ten_days_from_now])
#         dates = [schedule.date.strftime('%Y-%m-%d') for schedule in schedules]
#         response_data = {
#             'serviceId': pk,
#             'webSlug': web_slug,
#             'dates': dates
#         }
#         return JsonResponse(response_data)
#     elif request.method == 'POST':
#         if request.content_type == 'application/json':
#             data = json.loads(request.body)
#         else:
#             data = request.POST
#
#         service_id = data.get('serviceId')
#         web_slug = data.get('webSlug')
#         date_str = data.get('date')
#
#         service = get_object_or_404(Service, id=service_id, web=web)
#         doctor = service.doctors
#         schedules = DoctorSchedule.objects.filter(doctor=doctor)
#
#         if date_str:
#             try:
#                 date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
#                 schedule = schedules.filter(date=date).first()
#             except ValueError:
#                 return JsonResponse({'success': False, 'message': 'Invalid date format'})
#         else:
#             return JsonResponse({'success': False, 'message': 'Date is required'})
#
#         if schedule is None:
#             return JsonResponse({'success': False, 'message': 'No schedule found for the given date'})
#
#         appointment = Appointment.objects.filter(date=date, service=service, web=web)
#         appointment_times = set(appointment.values_list('time', flat=True))
#         available_times1 = []
#         available_times2 = []
#         timetaken = Decimal(doctor.timetaken)
#         for s in schedules:
#             first_period_start = s.first_period_start
#             first_period_end = s.first_period_end
#
#             second_period_start = s.second_period_start
#             second_period_end = s.second_period_end
#
#             timetaken = doctor.timetaken
#             Timetaken = timetaken + doctor.WaitTime
#             increment = datetime.timedelta(minutes=int(Timetaken))
#
#             current_time1 = datetime.datetime.combine(date, first_period_start)
#             current_time2 = datetime.datetime.combine(date, second_period_start)
#
#             while current_time1.time() <= first_period_end:
#                 if current_time1.time() not in appointment_times and current_time1.time() not in available_times1:
#                     available_times1.append(current_time1.time())
#                 current_time1 += increment
#
#             while current_time2.time() <= second_period_end:
#                 if current_time2.time() not in appointment_times and current_time2.time() not in available_times2:
#                     available_times2.append(current_time2.time())
#                 current_time2 += increment
#
#         available_times = []
#         for time in available_times1 + available_times2:
#             if time not in appointment_times and time not in available_times:
#                 available_times.append(time)
#
#         response_times = [time.strftime('%I:%M %p').replace('AM', 'ص').replace('PM', 'م') for time in available_times]
#
#         return JsonResponse({'success': True, 'available_times': response_times})

#
# def add_to_appointment(request, pk, web_slug):
#     web = get_object_or_404(WEB, slug=web_slug)
#     if request.method == 'GET':
#         service = get_object_or_404(Service, id=pk, web=web)
#         doctor = service.doctors
#         schedules = DoctorSchedule.objects.filter(doctor=doctor)
#         current_date = datetime.date.today()
#         ten_days_from_now = current_date + datetime.timedelta(days=10)
#         schedules = schedules.filter(date__range=[current_date, ten_days_from_now])
#         dates = [schedule.date.strftime('%Y-%m-%d') for schedule in schedules]
#         response_data = {
#             'serviceId': pk,
#             'webSlug': web_slug,
#             'dates': dates
#         }
#         return JsonResponse(response_data)
#     elif request.method == 'POST':
#         if request.content_type == 'application/json':
#             data = json.loads(request.body)
#
#         else:
#             data = request.POST
#
#         service_id = data.get('serviceId')
#         web_slug = data.get('webSlug')
#         date_str = data.get('date')
#         print('date_str',date_str)
#         service = get_object_or_404(Service, id=service_id, web=web)
#         doctor = service.doctors
#         schedules = DoctorSchedule.objects.filter(doctor=doctor, web=web)
#         # print('schedules',schedules)
#         if date_str:
#             try:
#                 date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
#                 schedule = schedules.filter(date=date,doctor=doctor, web=web).first()
#                 print('schedule',schedule)
#
#                 appointment = Appointment.objects.filter(date=date, service=service, web=web)
#         # print('appointment',appointment)
#                 appointment_times = set(appointment.values_list('time', flat=True))
#                 available_times1 = []
#                 available_times2 = []
#                 timetaken = Decimal(doctor.timetaken)
#
#
#                 first_period_start = schedule.first_period_start
#                 print('first_period_start',first_period_start)
#                 first_period_end = schedule.first_period_end
#                 print('first_period_end',first_period_end)
#                 second_period_start = schedule.second_period_start
#                 print('second_period_start',second_period_start)
#                 second_period_end = schedule.second_period_end
#                 print('second_period_end',second_period_end)
#
#                 timetaken = doctor.timetaken
#                 Timetaken = timetaken + doctor.WaitTime
#                 increment = datetime.timedelta(minutes=int(Timetaken))
#
#                 current_time1 = datetime.datetime.combine(date, first_period_start)
#
#                 while current_time1.time() <= first_period_end:
#                  if current_time1.time() not in appointment_times and current_time1.time() not in available_times1:
#                     available_times1.append(current_time1.time())
#                 current_time1 += increment
#                 available_times = available_times1
#
#
#
#                 current_time2 = None
#                 if second_period_start is not None or 00:
#                   current_time2 = datetime.datetime.combine(date, second_period_start)
#                 # print('current_time1',current_time1)
#
#                 if current_time2 is not None:
#                  while current_time2.time() <= second_period_end:
#                     if current_time2.time() not in appointment_times and current_time2.time() not in available_times2:
#                         available_times2.append(current_time2.time())
#                  current_time2 += increment
#                  available_times = available_times1 + available_times2
#
#                 else:
#                   print('NONE')
#
#
#         # print('available_times',available_times)
#                 response_times = [time.strftime('%I:%M %p').replace('AM', 'ص').replace('PM', 'م') for time in available_times]
#
#                 return JsonResponse({'success': True, 'available_times': response_times})
#
#
#             except ValueError:
#                 return JsonResponse({'success': False, 'message': 'Invalid date format'})
#         else:
#             return JsonResponse({'success': False, 'message': 'Date is required'})



def add_to_appointment(request, pk, web_slug):
    web = get_object_or_404(WEB, slug=web_slug)
    if request.method == 'GET':
        service = get_object_or_404(Service, id=pk, web=web)
        doctor = service.doctors
        schedules = DoctorSchedule.objects.filter(doctor=doctor)
        current_date = datetime.date.today()
        ten_days_from_now = current_date + datetime.timedelta(days=10)
        schedules = schedules.filter(date__range=[current_date, ten_days_from_now])
        dates = [schedule.date.strftime('%Y-%m-%d') for schedule in schedules]
        response_data = {
            'serviceId': pk,
            'webSlug': web_slug,
            'dates': dates
        }
        return JsonResponse(response_data)
    elif request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        service_id = data.get('serviceId')
        web_slug = data.get('webSlug')
        date_str = data.get('date')
        print('date_str',date_str)
        service = get_object_or_404(Service, id=service_id, web=web)
        doctor = service.doctors
        schedules = DoctorSchedule.objects.filter(doctor=doctor, web=web)

        if date_str:
            try:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                schedule = schedules.filter(date=date, doctor=doctor).first()
                print('schedule', schedule)

                appointment = Appointment.objects.filter(date=date, service=service, web=web)
                appointment_times = set(appointment.values_list('time', flat=True))
                available_times1 = []
                available_times2 = []
                timetaken = Decimal(doctor.timetaken)

                first_period_start = schedule.first_period_start
                print('first_period_start', first_period_start)
                first_period_end = schedule.first_period_end
                print('first_period_end', first_period_end)
                second_period_start = schedule.second_period_start
                print('second_period_start', second_period_start)
                second_period_end = schedule.second_period_end
                print('second_period_end', second_period_end)

                timetaken = doctor.timetaken
                Timetaken = timetaken + doctor.WaitTime
                increment = datetime.timedelta(minutes=int(Timetaken))

                current_time1 = datetime.datetime.combine(date, first_period_start)

                while current_time1.time() <= first_period_end:
                    if current_time1.time() not in appointment_times and current_time1.time() not in available_times1:
                        available_times1.append(current_time1.time())
                    current_time1 += increment

                print(current_time1)

                available_times = available_times1

                current_time2 = None
                if second_period_start:
                    current_time2 = datetime.datetime.combine(date, second_period_start)

                if current_time2 is not None:
                    while current_time2.time() <= second_period_end:
                        if current_time2.time() not in appointment_times and current_time2.time() not in available_times2:
                            available_times2.append(current_time2.time())
                        current_time2 += increment

                    available_times += available_times2

                response_times = [time.strftime('%I:%M %p').replace('AM', 'ص').replace('PM', 'م') for time in available_times]

                return JsonResponse({'success': True, 'available_times': response_times})

            except ValueError:
                return JsonResponse({'success': False, 'message': 'Invalid date format'})
        else:
            return JsonResponse({'success': False, 'message': 'Date is required'})


#
#
# def add_to_appointment(request, pk, web_slug):
#     web = get_object_or_404(WEB, slug=web_slug)
#     if request.method == 'GET':
#         service = get_object_or_404(Service, id=pk, web=web)
#         doctor = service.doctors
#         schedules = DoctorSchedule.objects.filter(doctor=doctor)
#         current_date = datetime.date.today()
#         ten_days_from_now = current_date + datetime.timedelta(days=10)
#         schedules = schedules.filter(date__range=[current_date, ten_days_from_now])
#         dates = [schedule.date.strftime('%Y-%m-%d') for schedule in schedules]
#         response_data = {
#             'serviceId': pk,
#             'webSlug': web_slug,
#             'dates': dates
#         }
#         return JsonResponse(response_data)
#     elif request.method == 'POST':
#         if request.content_type == 'application/json':
#             data = json.loads(request.body)
#         else:
#             data = request.POST
#
#         service_id = data.get('serviceId')
#         web_slug = data.get('webSlug')
#         date_str = data.get('date')
#         print('date_str',date_str)
#         service = get_object_or_404(Service, id=service_id, web=web)
#         doctor = service.doctors
#         schedules = DoctorSchedule.objects.filter(doctor=doctor, web=web)
#
#         if date_str:
#             try:
#                 date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
#                 schedule = schedules.filter(date=date, doctor=doctor).first()
#                 print('schedule', schedule)
#
#                 appointment = Appointment.objects.filter(date=date, service=service, web=web)
#                 appointment_times = set(appointment.values_list('time', flat=True))
#                 available_times1 = []
#                 available_times2 = []
#                 timetaken = Decimal(doctor.timetaken)
#
#                 first_period_start = schedule.first_period_start
#                 print('first_period_start', first_period_start)
#                 first_period_end = schedule.first_period_end
#                 print('first_period_end', first_period_end)
#                 second_period_start = schedule.second_period_start
#                 print('second_period_start', second_period_start)
#                 second_period_end = schedule.second_period_end
#                 print('second_period_end', second_period_end)
#
#                 timetaken = doctor.timetaken
#                 Timetaken = timetaken + doctor.WaitTime
#                 increment = datetime.timedelta(minutes=int(Timetaken))
#
#                 current_time1 = datetime.datetime.combine(date, first_period_start)
#
#                 while current_time1.time() <= first_period_end:
#                     if current_time1.time() not in appointment_times and current_time1.time() not in available_times1:
#                         available_times1.append(current_time1.time())
#                     current_time1 += increment
#
#                 print(current_time1)
#
#                 available_times = available_times1
#
#                 current_time2 = None
#                 if second_period_start:
#                     current_time2 = datetime.datetime.combine(date, second_period_start)
#
#                 if current_time2 is not None:
#                     while current_time2.time() <= second_period_end:
#                         if current_time2.time() not in appointment_times and current_time2.time() not in available_times2:
#                             available_times2.append(current_time2.time())
#                         current_time2 += increment
#
#                     available_times += available_times2
#
#                 response_times = [time.strftime('%I:%M %p').replace('AM', 'ص').replace('PM', 'م') for time in available_times]
#
#                 return JsonResponse({'success': True, 'available_times': response_times})
#
#             except ValueError:
#                 return JsonResponse({'success': False, 'message': 'Invalid date format'})
#         else:
#             return JsonResponse({'success': False, 'message': 'Date is required'})
