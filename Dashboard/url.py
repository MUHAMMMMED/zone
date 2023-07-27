from django.contrib import admin
from django.urls import path


from Dashboard.views.appointment import *
from Dashboard.views.category import *
from Dashboard.views.dashboard import *
from Dashboard.views.department import *
from Dashboard.views.doctor import *
from Dashboard.views.image import *
from Dashboard.views.insurance import *
from Dashboard.views.link import *
from Dashboard.views.Patient_profile import *
from Dashboard.views.Report import *
from Dashboard.views.section import *
from Dashboard.views.service import *
from Dashboard.views.question import *


app_name='Dashboard'


import string
import random




urlpatterns = [
    path('', dashboard, name='dashboard'),
    # path('settings/',Settings, name='Settings'),
    path('settings/', Settings, name='Settings'),
    path('report/', Report, name='Report'),
    path('create/', create_web, name='create_web'),
    path('web/<int:pk>/update/', update_web, name='web_update'),
    path('update_admin/<int:pk>/', update_web_admin, name='update_web_admin'),
    path('create_doctor/', create_doctor, name='create_doctor'),
    path('doctors/<int:doctor_id>/update/',  update_doctor, name='update_doctor'),
    path('doctor/<int:id>/delete_doctor/',  delete_doctor, name='delete_doctor'),
    path('create_section/', create_section, name='create_section'),
    path('section/<int:section_id>/update/',  update_section, name='update_section'),
    path('section/<int:id>/delete_section/',  delete_section, name='delete_section'),
    path('create_insurance/', create_insurance, name='create_insurance'),
    path('insurance/<int:insurance_id>/update/',  update_insurance, name='update_insurance'),
    path('insurance/<int:id>/delete_insurance/', delete_insurance, name='delete_insurance'),
    path('create_image/', create_image, name='create_image'),
    path('image/<int:image_id>/update/',  update_image, name='update_image'),
    path('image/<int:id>/delete_image/',  delete_image, name='delete_image'),
    path('create_question/', create_question, name='create_question'),
    path('question/<int:question_id>/update/',  update_question, name='update_question'),
    path('question/<int:id>/delete_question/',  delete_question, name='delete_question'),
    path('create_department/', create_department, name='create_department'),
    path('department/<int:department_id>/update/', update_department, name='update_department'),
    path('department/<int:id>/delete_department/',  delete_department, name='delete_department'),
    path('create_category/', create_category, name='create_category'),
    path('<int:pk>/update_category/', update_category, name='update_category'),
    path('categories/<int:pk>/delete/',delete_category, name='delete_category'),
    path('create_service/', create_service, name='create_service'),
    path('update_service/<int:service_id>/',update_service, name='update_service'),
    path('services/<int:id>/Service_delete/',  Service_delete, name='delete_service'),
    path('link/new/', create_link, name='link_new'),
    path('link/<int:pk>/edit/', update_link, name='link_edit'),
    path('create_nwe_appointment/', create_nwe_appointment, name='create_nwe_appointment'),
    path('NewBooking',NewBooking, name='NewBooking'),
    # path('add-to-cart/', add_to_cart, name='add_to_cart'),
    # path('delete_cart_items/<int:id>/', delete_cart_items_view, name='delete_cart_items'),
    # path('cart-items/', cart_items, name='cart_items'),
    # path('delete-from-cart/', delete_from_cart, name='delete_from_cart'),

    path('Dashboard/update_appointment/<int:id>/',  update_appointment, name='update_appointment'),

    path('Appointment_waiting/', Appointment_waiting, name='Appointment_waiting'),
    path('Appointment_notanswering/', Appointment_notanswering, name='Appointment_notanswering'),
    path('Appointment_confirmed/', Appointment_confirmed, name='Appointment_confirmed'),
    path('Appointment_inquiries/', Appointment_inquiries, name='Appointment_inquiries'),
    path('Appointment_cancel/', Appointmentcancel, name='Appointment_cancel'),
    path('Appointment_visit/', Appointment_visit, name='Appointment_visit'),
    path('Dashboard/Patient_profile/<int:id>/', Patient_profile, name='Patientprofile'),
    path('patients/<int:patient_id>/update/', update_patient, name='update_patient'),
    path('update_status/', update_status, name='update_status'),
    # path('report/', Report, name='Report'),
    path('delete_service/<int:service_id>/<int:appointment_id>/', delete_service, name='delete_service'),
    path('visitstoday/',  Visitstoday, name='visitstoday'),
    path('appointments_1_hours_ago/',  appointments_1_hours_ago, name='appointments_1_hours_ago'),
    path('appointments_3_hours_ago/',  appointments_3_hours_ago, name='appointments_3_hours_ago'),
    path('appointments/later/', appointments_later, name='appointments_later'),
    path('missedreservation/',  missedreservation, name='missedreservation'),
    path('doctor/<int:id>/', Doctor_profile_view, name='DoctorProfile'),
    path('schedule/update/<int:schedule_id>/', update_schedule, name='update_schedule'),
    path('schedule/<int:schedule_id>/delete/', delete_schedule, name='delete_schedule'),
    path('add_to_appointment/<int:pk>/<slug:web_slug>/', add_to_appointment, name='add_to_appointment'),
    path('NEW_appointment/', NEW_appointment, name='NEW_appointment'),

 


]
