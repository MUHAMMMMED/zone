from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from webs.views.Home import *
from webs.views.Links import *
from webs.views.Doctor import *
from webs.views.categories import *
from webs.views.Appointment import *
from webs.views.Services import *
from webs.views.confirmation import *
from webs.views.pixel import *





app_name='webs'
urlpatterns = [
 path('',home, name="home"),

  path('<slug:web_slug>/',  web, name='web'),

  path('web/<slug:web_slug>/doctors/', doctor, name='doctor'),

  path('web/<slug:web_slug>/doctors/<int:doctor_id>/', doctor_detail, name='doctor_detail'),

  path('<slug:web_slug>/categories/<int:id>/', categories, name='categories'),

  path('services/<int:id>/', services, name="service"),

  # path('add-to-cart/<int:id>/', add_to_cart, name='add_to_cart'),

  # path('<slug:web_slug>/cart_and_checkout/', cart_and_checkout, name='cart_and_checkout'),

  path('<slug:web_slug>/SocialMediaLinks', view_links, name='SocialMediaLinks'),

  path('<slug:web_slug>/category/<int:category_id>/service/<int:service_id>/', services, name='service'),
    # ... other URL patterns ...
  path('booking_confirmation/<slug:web_slug>/',  booking_confirmation, name='booking_confirmation'),
    # other URL patterns ...
  path('<slug:web_slug>/categories-services/', categories_services, name='categories_services'),
    # other URL patterns ...
    # other URL patterns here
  # path('cart-item/refresh/', cart_item_refresh_view, name='cart_item_refresh'),
  #
  #
  # path('cart-item/delete/', cart_item_delete_view, name='cart_item_delete'),






    path('<slug:web_slug>/pixel_data/', pixel_data, name='pixel_data'),



    path('add_to_appointment/<int:pk>/<slug:web_slug>/', add_to_appointment, name='add_to_appointment'),

# pixel



    path('web/<slug:web_slug>/increment_click_whatsapp/',  increment_click_web_whatsapp, name='increment_click_web_whatsapp'),


    path('all_category/<slug:web_slug>/increment_click_whatsapp/',  increment_click_all_category_whatsapp, name='increment_click_all_category_whatsapp'),
    path('category/<int:category_id>/<slug:web_slug>/increment_click_whatsapp/',  increment_click_category_whatsapp, name='increment_click_category_whatsapp'),

    path('Doctors/<slug:web_slug>/increment_click_web_whatsapp/',  increment_click_Doctors_whatsapp, name='increment_click_Doctors_whatsapp'),
    # path('Doctors_details_/<int:doctor_id>/increment_click_whatsapp/',  increment_click_Doctors_details_whatsapp, name='increment_click_Doctors_details_whatsapp'),

    path('services/<slug:web_slug>/<int:service_id>/increment_click_whatsapp/',  increment_click_service_whatsapp, name='increment_click_service_whatsapp'),


    path('Doctors_details_/<int:doctor_id>/<slug:web_slug>/increment_click_whatsapp/',  increment_click_Doctors_details_whatsapp, name='increment_click_Doctors_details_whatsapp'),


]
