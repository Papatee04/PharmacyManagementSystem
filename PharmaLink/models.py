from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now
from django.utils import timezone
from phonenumber_field.formfields import PhoneNumberField
from datetime import timedelta


class Drug(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    strength = models.CharField(max_length=50, null=True, blank=True)
    dosage = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='drug_photos', null=True, blank=True)

    # You can add more fields as needed, like dosage, side effects, etc.

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    # User type choices
    user_type_data = ((1, "AdminHOD"), (2, "Pharmacist"), (3, "Doctor"), (5, "Patients"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

    # Common attributes for all user types
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=7, choices=[('Male', 'Male'), ('Female', 'Female')], null=True, blank=True)
    age = models.IntegerField(default=0, blank=True, null=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)


    def __str__(self):
        return str(self.username)

class Patients(models.Model):
    # Inherit from CustomUser
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=30, null=True, blank=True, unique=True)
    dob = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.admin)


class AdminHOD(models.Model):
    # Inherit from CustomUser
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    employee_no = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.admin)

class Pharmacist(models.Model):
    # Inherit from CustomUser
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    employee_no = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.admin)


class Doctor(models.Model):
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    emp_no = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    specialisation = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.admin)

	   

class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)
    
    def __str__(self):
        return str(self.name)
	

    
def default_valid_till_date():
    return timezone.now() + timedelta(days=30)

class Prescription(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, null=True, blank=True)
    patient_id = models.ForeignKey(Patients, null=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True)
    date_precribed = models.DateTimeField(default=timezone.now)
    valid_till_date = models.DateField(default=default_valid_till_date)
    doctor_issued = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    


class ExpiredManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
        )

class Inventory(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category,null=True,on_delete=models.CASCADE,blank=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    valid_from = models.DateTimeField(blank=True, null=True,default=timezone.now)
    valid_to = models.DateTimeField(blank=False, null=True)
    objects = ExpiredManager()
   
    def __str__(self):
        return str(self.drug_name)
   
    
class Dispense(models.Model):
    
    patient_id = models.ForeignKey(Patients, on_delete=models.DO_NOTHING,null=True)
    drug = models.ForeignKey(Drug, on_delete=models.SET_NULL, null=True, blank=True)
    dispense_quantity = models.PositiveIntegerField(default='1', blank=False, null=True)
    instructions=models.CharField(max_length=300,null=True, blank=False)
    dispense_at = models.DateTimeField(blank=True, null=True,default=timezone.now)
    prescription = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True, blank=True)





@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Pharmacist.objects.create(admin=instance,address="")
        if instance.user_type == 3:
            Doctor.objects.create(admin=instance,address="")
        if instance.user_type == 5:
            Patients.objects.create(admin=instance,address="")
       
       
       

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.pharmacist.save()
    if instance.user_type == 3:
        instance.doctor.save()
    if instance.user_type == 5:
        instance.patients.save()


   



 