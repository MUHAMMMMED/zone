import os
# Create your views here.






from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
# # from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from datetime import date, datetime, timedelta
import calendar


from webs.models import *
from Dashboard.forms import *
from webs.form import *
from Dashboard.filters import *



 #  start Doctor
@login_required

def create_doctor(request):
    # Retrieve the WEB instance that the doctor will be related to
    user = User.objects.get(id=request.user.id)
    categories = Categories.objects.filter(web__Employee_WEB=user)

    if request.method == 'POST':
        # If the form has been submitted, create a new instance and save it
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            web = WEB.objects.filter(Employee_WEB=request.user).first()

            new_doctor = form.save(commit=False)
            category_id = request.POST['category_id']
            category = Categories.objects.get(id=category_id)
            new_doctor.category_id = category
            new_doctor.web = web
            new_doctor.save()
            return redirect('Dashboard:dashboard')
    else:
        # If the form has not been submitted, display the form
        form = DoctorForm()

    # Render the template with the form and the WEB instance
    title = 'اضافه دكتور جديد'
    context = {'form': form, 'title': title, 'categories': categories}
    return render(request, 'create_doctor.html', context)



@login_required
def update_doctor(request, doctor_id):
    # Get the Doctor object with the given id
    doctor = get_object_or_404(Doctors, id=doctor_id)
    user = User.objects.get(id=request.user.id)
    categories = Categories.objects.filter(web__Employee_WEB=user)

    if request.method == 'POST':
        # Create a form instance with the submitted data and the Doctor object as the instance to update
            form = DoctorForm(request.POST, request.FILES, instance=doctor)

            web = WEB.objects.filter(Employee_WEB=request.user).first()

            form = form.save(commit=False)
            category_id = request.POST['category_id']
            category = Categories.objects.get(id=category_id)
            form.category_id = category
            form.web = web

            # Save the updated Doctor object
            form.save()
            return redirect('Dashboard:dashboard')
    else:
        # Create a form instance with the Doctor object to pre-fill the form
        form = DoctorForm(instance=doctor)

    # Render the update doctor page with the form and doctor object
    title='  تحديث بيانات الدكتور    '
    context = {'form': form, 'title':title ,'doctor':doctor,'categories':categories}
    return render(request, 'update_doctor.html', context)



@login_required
def delete_doctor(request, id):
    doctor = Doctors.objects.get(id=id)
    if request.method == 'POST':
        doctor.delete()
        return redirect('Dashboard:dashboard')
    context = {'doctor': doctor}
    return render(request, 'delete_service.html', context)







 # /===========================

@login_required

def Doctor_profile_view(request, id):
     user = User.objects.get(id=request.user.id)
     weB = WEB.objects.filter(Employee_WEB=user).first()
     doctor = get_object_or_404(Doctors, id=id, web=weB)
     print('doctor',doctor)
     my_queryset = DoctorSchedule.objects.filter(doctor=doctor )
     message = ''
     if 'DoctorSchedule-form' in request.POST:
         day_of_week = request.POST.get('day_of_week')
         start_month = int(request.POST.get('start_month'))
         end_month = int(request.POST.get('end_month'))
         start_time_str = request.POST.get('start_time')
         end_time_str = request.POST.get('end_time')
         second_start_time_str = request.POST.get('second_start_time')
         second_end_time_str = request.POST.get('second_end_time')
         year = int(request.POST.get('year'))
         print('ok')
         if start_time_str and end_time_str:
             start_time = datetime.strptime(start_time_str, '%H:%M').time()
             print('start_time',start_time)
             end_time = datetime.strptime(end_time_str, '%H:%M').time()
             print('end_time',end_time)
             if second_start_time_str and second_end_time_str:
                 second_start_time = datetime.strptime(second_start_time_str, '%H:%M').time()
                 second_end_time = datetime.strptime(second_end_time_str, '%H:%M').time()
                 message = save_dates_for_day_and_time(weB,doctor,year,start_month,end_month,day_of_week,start_time,end_time,second_start_time,second_end_time)
             else:
                 # Create appointments for the first time slot only
                 second_start_time = None
                 second_end_time = None
                 message = save_dates_for_day_and_time(weB,doctor,year,start_month,end_month,day_of_week,start_time,end_time,second_start_time,second_end_time)
     elif 'form2_submit' in request.POST:
         Date = request.POST.get('date')
         if Date:
             # Get the DoctorSchedule objects for the specified date

             my_queryset = DoctorSchedule.objects.filter(doctor=doctor ,date=Date)
         else:
             message = "Please provide a date"
     elif 'Delete_submit' in request.POST:
         start_date = request.POST.get('start_date')
         end_date = request.POST.get('end_date')
         schedule = DoctorSchedule.objects.filter(date__range=[start_date, end_date],doctor=doctor)
         schedule.delete()
     else:
         my_queryset = DoctorSchedule.objects.filter(doctor=doctor)
         # message = 'Please submit the form to create or delete appointments.'

     today = date.today()
     year = today.year
     month = today.month
     first_day = date(year, month, 1)
     last_day = date(year, month, 1).replace(month=month+1) - timedelta(days=1)
     days_in_month = (last_day - first_day).days + 1

     # Get all DoctorSchedule objects for the current month and doctor
     dates_with_data = DoctorSchedule.objects.filter(date__year=year, date__month=month, doctor=doctor)

     # Create a dictionary of DoctorSchedule objects by day of the month
     data_by_day = {d.date.day: d for d in dates_with_data}

     # List of weekday names in Arabic
     weekday_names = ['الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']

     # List of dictionaries representing each day in the current month
     days = []
     for i in range(days_in_month):
         day_num = i + 1
         day = first_day + timedelta(days=i)
         active_class = ''
         if day_num in data_by_day:
             active_class = 'active'
         # Get the weekday name for the current day
         weekday_name = weekday_names[day.weekday()]
         days.append({
             'day': day_num,
             'date': day,
             'active_class': active_class,
             'weekday': weekday_name,
         })

     # Sort the days by date in ascending order, and then by day number in ascending order
     days.sort(key=lambda d: (d['date'], d['day']))

     context = {
         'doctor': doctor,
         'my_queryset': my_queryset,
         'message': message,
         'days': days,
         'month_name': first_day.strftime('%B'),
         'year': year,
         'weekday_names': weekday_names,
     }

     return render(request, 'doctor_profile.html', context)

from django.utils import timezone


def save_dates_for_day_and_time(weB, doctor, year, start_month, end_month, day_of_week, start_time, end_time, second_start_time, second_end_time):
    current_date = datetime(year, start_month, 1).date()
    end_date = datetime(year, end_month, 1).date()

    while current_date <= end_date:
        if current_date.strftime('%a').upper() == day_of_week:
            start_datetime = datetime.combine(current_date, start_time)
            end_datetime = datetime.combine(current_date, end_time)

            if second_start_time is not None:
                second_start_datetime = datetime.combine(current_date, second_start_time)
                second_end_datetime = datetime.combine(current_date, second_end_time)
            else:
                second_start_datetime = None
                second_end_datetime = None
            print('weB',weB)
            print('doctor',doctor)
            print('day_of_week',day_of_week)
            print('current_date',current_date)
            print('start_datetime',start_datetime)
            print('end_datetime',end_datetime)
            print('second_start_datetime',second_start_datetime)
            print('second_end_datetime',second_end_datetime)
            DS=DoctorSchedule.objects.filter(web=weB, doctor=doctor, date=current_date)
            print('DoctorSchedule',DS)
            # Check if a DoctorSchedule instance with the same date, web, and doctor already exists


            # Check if a DoctorSchedule instance with the same date, web, and doctor already exists
            existing_schedule = DoctorSchedule.objects.filter(web=weB, doctor=doctor, date=current_date).first()

            if existing_schedule:
                # Update the existing DoctorSchedule instance with the new values
                existing_schedule.first_period_start = start_datetime
                existing_schedule.first_period_end = end_datetime
                existing_schedule.second_period_start = second_start_datetime
                existing_schedule.second_period_end = second_end_datetime
                existing_schedule.save()
            else:
                # Create a new DoctorSchedule instance
                DoctorSchedule.objects.create(
                    web=weB,
                    doctor=doctor,
                    day_of_week=day_of_week,
                    date=current_date,
                    first_period_start=start_datetime,
                    first_period_end=end_datetime,
                    second_period_start=second_start_datetime,
                    second_period_end=second_end_datetime
                )

        current_date += timedelta(days=1)

    return "Dates saved successfully"



def delete_schedule(request, schedule_id):
     # Retrieve the DoctorSchedule instance to be deleted
     schedule = get_object_or_404(DoctorSchedule, id=schedule_id)
     id=schedule.doctor.id
     if request.method == 'POST':
         # Call the delete() method on the instance to delete it from the database
         schedule.delete()
         # Redirect back to the DoctorProfile view with the same doctor ID

         return redirect('Dashboard:DoctorProfile', id=id )

     # Render the confirmation page to confirm the deletion
     return render(request, 'delete_service.html', {'schedule': schedule})



def update_schedule(request, schedule_id):
     # Retrieve the DoctorSchedule instance to be updated
     schedule = get_object_or_404(DoctorSchedule, id=schedule_id)
     id=schedule.doctor.id
     if request.method == 'POST':
         # Create a form instance with the POST data and the instance to be updated
         form = DoctorScheduleForm(request.POST, instance=schedule)
         if form.is_valid():
             # Save the updated instance
             form.save()
             # Redirect back to the DoctorProfile view for the same Doctor instance
             return redirect('Dashboard:DoctorProfile', id=id )
     else:
         # Create a form instance initialized with the instance to be updated
         form = DoctorScheduleForm(instance=schedule)

     # Render the update schedule page with the form and the schedule instance as context data
     return render(request, 'update_schedule.html', {'form': form, 'schedule': schedule})
