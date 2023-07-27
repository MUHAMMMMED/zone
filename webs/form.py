from django import forms
from webs.models import *

from django.forms import ModelForm



class BookingForm(forms.ModelForm):
    name = forms.CharField(label='الاسم')
    phone = forms.CharField(label='رقم الهاتف')
    knew_from = forms.ChoiceField(label='كيف عرفت عنا', choices=Appointment.CHOICES_knew, required=False)
    note = forms.CharField(label='ملاحظات', widget=forms.Textarea(attrs={'rows': 3}), help_text='أدخل أي ملاحظات هنا')

    class Meta:
        model = Appointment
        fields = ('name', 'phone', 'knew_from', 'note')
        exclude = ['web', 'service', 'status_appointment','ClientStatus', 'price','serviceName']



class AppointmentForm(forms.ModelForm):
    name = forms.CharField(label='الاسم')
    phone = forms.CharField(label='رقم الهاتف')
    # ClientStatus = forms.ChoiceField(label='حالة العميل', choices=Appointment.CHOICES_clientstatus, required=False)
    knew_from = forms.ChoiceField(label='كيف عرفت عنا', choices=Appointment.CHOICES_knew, required=False)
    note = forms.CharField(label='ملاحظات', widget=forms.Textarea(attrs={'rows': 4}), help_text='أدخل أي ملاحظات هنا')

    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='التاريخ')
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='الوقت')



    class Meta:
        model = Appointment
        fields = ('name', 'phone', 'knew_from', 'note', 'date', 'time')
        exclude = ('web', 'service', 'ClientStatus', 'status_appointment',)







class update_AppointmentForm(forms.ModelForm):
    name = forms.CharField(label='الاسم')
    # ClientStatus = forms.ChoiceField(label='حالة العميل', choices=Appointment.CHOICES_clientstatus, required=False)
    note = forms.CharField(label='ملاحظات', widget=forms.Textarea(attrs={'rows': 2}),  )


    class Meta:
        model = Appointment
        fields = ('name', 'phone',  'knew_from', 'note')
        exclude = ('web', 'service','status_appointment','knew_from',  'ClientStatus','date', 'time')





class PatientForm(ModelForm):
    Detailedaddress = forms.CharField(label='address', widget=forms.Textarea(attrs={'rows': 3}) )

    class Meta:
        model = Patient
        fields = ['name','age', 'gender', 'FileNnumber', 'phone', 'Detailedaddress']
        exclude = ('web',)


class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ['doctor', 'day_of_week', 'date', 'first_period_start', 'first_period_end', 'second_period_start', 'second_period_end']
