from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# # Register your models here.
admin.site.register(WEB)
admin.site.register(Doctors)
admin.site.register(DoctorSchedule)
admin.site.register(Categories)
admin.site.register(Service)
admin.site.register(Doctors_pixel)
admin.site.register(Categories_pixel)
admin.site.register(Service_pixel)
admin.site.register(pixel)



@admin.register(Appointment)
class BookingAdmin(ImportExportModelAdmin):

    model = Appointment
#     # model = Booking
#     # list_display = ['created_at','name' , 'phone','Message','web','knew' ]
#     # list_filter = ( 'created_at','name' , 'phone','Message','web','knew' )
