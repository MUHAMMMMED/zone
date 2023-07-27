from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from Users.models import *





# models.py

from django.db import models
from django.contrib.sessions.models import Session


class WEB(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    Employee_WEB = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee', blank=True, null=True)
    active = models.BooleanField(default=False)
    slug = models.CharField(max_length=50, unique=True, blank=True, null=True)
    FaviconIco= models.FileField(upload_to = "files/images/WEB/FaviconIco/%Y/%m/%d/",blank=True, null=True)
    logo = models.FileField(upload_to = "files/images/WEB/logo/%Y/%m/%d/",blank=True, null=True)
    keywords= models.CharField(max_length = 300,blank=True, null=True)
    pixal_id= models.CharField(max_length=500,blank=True, null=True)
    Title = models.CharField(max_length=100,blank=True, null=True)
    Title_logo = models.FileField(upload_to = "files/images/WEB/Title_logo/%Y/%m/%d/",blank=True, null=True)
    silderImage = models.FileField(upload_to = "files/images/WEB/silderImage/%Y/%m/%d/",blank=True, null=True)
    info = models.CharField(max_length = 300 ,blank=True, null=True)
    Description= models.CharField(max_length = 300 ,blank=True, null=True)
    PHONE = models.CharField(max_length = 300 ,blank=True, null=True)
    Whatsapp= models.CharField(max_length=500,blank=True, null=True)
    linkedinlinke= models.CharField(max_length=500,blank=True, null=True)
    snapchat= models.CharField(max_length=500,blank=True, null=True)
    instagramlinke= models.CharField(max_length=500,blank=True, null=True)
    Twitterlinke= models.CharField(max_length=500,blank=True, null=True)
    facebooklinke= models.CharField(max_length=500,blank=True, null=True)
    OpeningHours= models.CharField(max_length=500,blank=True, null=True)
    Address= models.CharField(max_length=500,blank=True, null=True)
    Map_Address= models.CharField(max_length=500,blank=True, null=True)
    callـcountryـcode= models.IntegerField(blank=True, null=True)
    currencyـname=models.CharField(max_length = 300 ,blank=True, null=True)

    settings_password= models.CharField(max_length = 300 ,blank=True, null=True)
    Appointment_password= models.CharField(max_length = 300 ,blank=True, null=True)
    Report_password= models.CharField(max_length = 300 ,blank=True, null=True)

 
    def __str__(self):
         return self.slug

    def delete(self, *args, **kwargs):
        self.FaviconIco.delete()
        self.logo.delete()
        self.Title_logo.delete()
        self.silderImage.delete()

        super().delete(*args, **kwargs)







class pixel(models.Model):
     # created_at = models.DateTimeField(auto_now_add=True)
     date = models.DateField( blank=True, null=True)
     web=models.ForeignKey(WEB,on_delete=models.CASCADE, related_name='pixel', blank=True, null=True)
     views_Home = models.IntegerField(default=0,blank=True, null=True)
     click_whatsapp_Home = models.IntegerField(default=0,blank=True, null=True)
     views_Allcategories = models.IntegerField(default=0,blank=True, null=True)
     click_whatsapp_Allcategories = models.IntegerField(default=0,blank=True, null=True)
     views_Confirmation = models.IntegerField(default=0,blank=True, null=True)
     click_whatsapp_Doctor = models.IntegerField(default=0,blank=True, null=True)
     view_Doctor = models.IntegerField(default=0,blank=True, null=True)
     views_Link_page= models.IntegerField(default=0,blank=True, null=True)





class Link(models.Model):
      web=models.ForeignKey(WEB,on_delete=models.CASCADE, related_name='link', blank=True, null=True)
      info = models.CharField(max_length = 500 ,blank=True, null=True)
      hour= models.CharField(max_length = 300 ,blank=True, null=True)
      weblinke = models.CharField(max_length = 300 ,blank=True, null=True)
      PHONElinke  = models.CharField(max_length = 300 ,blank=True, null=True)
      Whatsapplinke= models.CharField(max_length=500,blank=True, null=True)
      linkedinlinke= models.CharField(max_length=500,blank=True, null=True)
      snapchatlinke= models.CharField(max_length=500,blank=True, null=True)
      instagramlinke= models.CharField(max_length=500,blank=True, null=True)
      Twitterlinke= models.CharField(max_length=500,blank=True, null=True)
      facebooklinke= models.CharField(max_length=500,blank=True, null=True)
      youtubelinke= models.CharField(max_length=500,blank=True, null=True)




class Department(models.Model):
    web=models.ForeignKey(WEB,on_delete=models.CASCADE, related_name='department', blank=True, null=True)
    name = models.CharField(max_length=100)


class Questions(models.Model):
    web = models.ForeignKey(WEB, related_name='qestions', on_delete=models.CASCADE)
    question= models.CharField(max_length = 300 ,blank=True, null=True)
    answer = models.CharField(max_length=300,blank=True, null=True)
    def __str__(self):
         return self.question

#
class Image(models.Model):
   web=models.ForeignKey(WEB,on_delete=models.CASCADE, related_name='image', blank=True, null=True)
   image = models.FileField(upload_to = "files/images/WEB/Image/%Y/%m/%d/",blank=True, null=True)
   imagename = models.CharField(max_length = 300 ,blank=True, null=True)
   def __str__(self):
         return self.imagename

   def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


#
class Insurance(models.Model):
   web=models.ForeignKey(WEB,on_delete=models.CASCADE, related_name='insurance', blank=True, null=True)
   name = models.CharField(max_length = 300 ,blank=True, null=True)
   def __str__(self):
         return self.name
#
class Section(models.Model):
   web=models.ForeignKey(WEB,on_delete=models.CASCADE, related_name='section', blank=True, null=True)
   name = models.CharField(max_length = 300 ,blank=True, null=True)
   image = models.FileField(upload_to = "files/images/WEB/Section/%Y/%m/%d/",blank=True, null=True)


   def __str__(self):
         return self.name



# __________________________________

class Categories(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    keywords = models.CharField(max_length=300, blank=True, null=True)
    Image = models.FileField(upload_to="files/images/WEB/Categories/%Y/%m/%d/", blank=True, null=True)
    Name = models.CharField(max_length=300, blank=True, null=True)
    web = models.ForeignKey(WEB, on_delete=models.CASCADE, related_name='categories', blank=True, null=True)
    # views = models.IntegerField(default=0,blank=True, null=True)
    # Click_whatsapp= models.IntegerField(default=0,blank=True, null=True)
    def __str__(self):
        return self.Name
    #
    def delete(self, *args, **kwargs):
        self.Image.delete()
        super().delete(*args, **kwargs)

class Categories_pixel(models.Model):

     date = models.DateField( blank=True, null=True)
     web=models.ForeignKey(WEB,on_delete=models.CASCADE,related_name='Categories', blank=True, null=True)
     CategoryName = models.CharField(max_length=100, blank=True, null=True)
     views= models.IntegerField(default=0,blank=True, null=True)
     click_whatsapp= models.IntegerField(default=0,blank=True, null=True)
     booking= models.IntegerField(default=0,blank=True, null=True)






class Doctors(models.Model):
   created_at = models.DateTimeField(auto_now_add=True)
   active = models.BooleanField(default=False)
   web=models.ForeignKey(WEB,on_delete=models.CASCADE, related_name='doctors', blank=True, null=True)
   Image = models.FileField(upload_to = "files/images/WEB/Doctors/%Y/%m/%d/",blank=True, null=True)
   Name = models.CharField(max_length = 300 ,blank=True, null=True)
   jobtitle= models.CharField(max_length = 300 ,blank=True, null=True)
   price = models.DecimalField(max_digits=10, decimal_places=2)
   category_id=models.ForeignKey(Categories,on_delete=models.CASCADE, related_name='Doctors', blank=True, null=True)
   timetaken = models.DecimalField(max_digits=10, decimal_places=2, default=0)
   WaitTime= models.DecimalField(max_digits=10, decimal_places=2, default=0)



   def delete(self, *args, **kwargs):
        self.Image.delete()
        super().delete(*args, **kwargs)

   # def __str__(self):
   #      return f"{self.Name} ({self.jobtitle})"

   def __str__(self):
        return self.Name


class Doctors_pixel(models.Model):

     date = models.DateField( blank=True, null=True)
     web=models.ForeignKey(WEB,on_delete=models.CASCADE, related_name='Doctors', blank=True, null=True)
     DoctorName = models.CharField(max_length=100, blank=True, null=True)
     views= models.IntegerField(default=0,blank=True, null=True)
     click_whatsapp= models.IntegerField(default=0,blank=True, null=True)
     booking= models.IntegerField(default=0,blank=True, null=True)






class DoctorSchedule(models.Model):
   DAY_CHOICES = [
                ('MON', 'Monday'),
                ('TUE', 'Tuesday'),
                ('WED', 'Wednesday'),
                ('THU', 'Thursday'),
                ('FRI', 'Friday'),
                ('SAT', 'Saturday'),
                ('SUN', 'Sunday'),
            ]
   doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, related_name='doctor_Appointments')
   day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES, blank=True, null=True)
   date = models.DateField()
   first_period_start = models.TimeField()
   first_period_end = models.TimeField()
   second_period_start = models.TimeField(blank=True, null=True)
   second_period_end = models.TimeField(blank=True, null=True)
   web=models.ForeignKey(WEB,on_delete=models.CASCADE, related_name='DoctorSchedule')

   # def __str__(self):
   #       return self.date


class Service(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    web=models.ForeignKey(WEB,on_delete=models.CASCADE, related_name='Service', blank=True, null=True)
    category_id=models.ForeignKey(Categories,on_delete=models.CASCADE, related_name='Services', blank=True, null=True)
    doctors=models.ForeignKey(Doctors,on_delete=models.CASCADE, related_name='doctors', blank=True, null=True)
    keywords = models.CharField(max_length=300, blank=True, null=True)
    Image = models.FileField(upload_to="files/images/WEB/Service/%Y/%m/%d/", blank=True, null=True)
    Title = models.CharField(max_length=100)
    Description = models.CharField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    long_image = models.FileField(upload_to = "files/images/WEB/Service/long/%Y/%m/%d/",blank=True, null=True)

    #
    # def __str__(self):
    #     return self.Title

    def delete(self, *args, **kwargs):
        self.Image.delete()
        self.long_image.delete()
        super().delete(*args, **kwargs)





    def calculate_sale_price(self):
        discount_amount = self.price * (self.discount_percentage / 100)
        self.sale_price = self.price - discount_amount
        return self.sale_price


class Service_pixel(models.Model):
    date = models.DateField(blank=True, null=True)
    web = models.ForeignKey( WEB,on_delete=models.CASCADE,related_name='service_pixels', blank=True,null=True    )

    ServiceName = models.CharField(max_length=100, blank=True, null=True)
    views = models.IntegerField(default=0, blank=True, null=True)
    click_whatsapp = models.IntegerField(default=0, blank=True, null=True)
    booking = models.IntegerField(default=0, blank=True, null=True)


class Patient(models.Model):
    Undefined='غير محدد'
    Male = 'ذكر '
    female = 'انثى'

    date_joined =models.DateTimeField(auto_now_add=True)
    CHOICES_Type = ((Undefined,'غير محدد'),(Male,'ذكر'),(female,'انثى') )
    web = models.ForeignKey(WEB, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    FileNnumber = models.IntegerField( blank=True, null=True)
    gender = models.CharField(max_length=30, choices=CHOICES_Type, blank=True, null=True)
    phone = models.IntegerField(null=True )
    age = models.IntegerField(null=True )
    Detailedaddress= models.CharField(max_length=500, blank=True, null=True)
    # def __str__(self):
    #      return self.web





class Appointment(models.Model):

    Undefined = "كيف عرفتنا"
    insurance = 'تأمين'
    Friend = 'صديق '
    family = 'أسرة'
    neighbors = 'الجيران'
    Google = 'جوجل '
    Whatsapp = 'واتساب'
    snapchat = 'سناب'
    Instagram = 'انستقرام'
    Twitter = 'تويتر'
    Facebook = 'فيس بوك '
    ticktock = 'تيك توك'
    YouTube = 'يوتيوب '
    Email = 'البريد الإلكتروني'
    Site = 'موقع'
    other = 'آخر'

    CHOICES_knew = (
        (Undefined, "كيف عرفتنا"),
        (insurance, 'تأمين'),
        (Friend, 'صديق '),
        (family, 'أسرة'),
        (neighbors, 'الجيران'),
        (Google, 'جوجل '),
        (Whatsapp, 'واتساب'),
        (snapchat, 'سناب'),
        (Instagram, 'انستقرام'),
        (Twitter, 'تويتر'),
        (Facebook, 'فيس بوك '),
        (ticktock, 'تيك توك'),
        (YouTube, 'يوتيوب '),
        (Email, 'البريد الإلكتروني'),
        (Site, ' موقع الإلكتروني'),
        (other, 'آخر'),
    )

    waiting = 'انتظار'
    Inquiries="الاستفسار"
    notanswering= 'عدم الرد'
    cancel ='إلغاءحجزه'
    confirmed="حجز مؤكد"
    missed_reservation= 'حجز فائت'
    Visit =  'حضر'

    Undefined='غير محدد'
    New = 'جديد'
    Old = 'قديم'
    CHOICES_clientstatus = ((Undefined,'غير محدد'),(New,'جديد'),(Old,'قديم'))

    STATUS_CHOICES = (('waiting','انتظار'),('inquiries', 'الاستفسار'),('cancel', 'إلغاءحجزه'),('notanswering', 'عدم الرد'),('confirmed', 'حجز مؤكد'),('missed_reservation', 'حجز فائت'),   ('visit', 'حضر'),)
    created_at = models.DateTimeField(auto_now_add=True)
    ClientStatus=models.CharField( max_length=30, choices=CHOICES_clientstatus, default=Undefined ,blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.IntegerField(null=True)
    patient = models.ForeignKey(Patient, related_name='patient_appointments', on_delete=models.CASCADE,blank=True, null=True)
    doctor_id=models.ForeignKey(Doctors,on_delete=models.CASCADE, related_name='doctors_Appointment', blank=True, null=True)
    category_id=models.ForeignKey(Categories,on_delete=models.CASCADE, related_name='categoryـAppointment', blank=True, null=True)
    service=models.ForeignKey(Service,on_delete=models.CASCADE, related_name='Service_Appointment', blank=True, null=True)
    serviceName=models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    web = models.ForeignKey(WEB, on_delete=models.CASCADE, blank=True, null=True)
    knew_from = models.CharField(max_length=50, choices=CHOICES_knew, blank=True, null=True)
    status_appointment =models.CharField(max_length=30, choices=STATUS_CHOICES , default=waiting)
    note = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField( blank=True, null=True)
    time = models.TimeField( blank=True, null=True)

    def __str__(self):
         return self.name
