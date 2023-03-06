from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.db import models
from .managers import CustomAccountManager


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"
        ordering = ('-created',)
        

    def __str__(self):
        return self.email
    
    
class Doctor(models.Model):
    doc_name = models.CharField(max_length=150)
    doc_email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=20)
    job_title = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.doc_name

    
class Patient(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='patient', on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=150)
    patient_id = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=20)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    admission_date = models.DateField()
    discharge_date = models.DateField(null=True, blank=True)
    pass_text = models.CharField(max_length=130, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Patients"
        verbose_name_plural = "Patients"
        ordering = ('-created',)

    def __str__(self):
        return self.full_name
    

class Billing(models.Model):
    patient = models.ForeignKey(Patient, related_name='billing', on_delete=models.CASCADE)
    report_summary = models.TextField()
    days_spent = models.IntegerField(null=True, blank=True)
    billing_date = models.DateField()
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.patient.full_name

