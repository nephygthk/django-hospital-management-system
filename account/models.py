import math
import random
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.db import models
from .managers import CustomAccountManager
from decimal import Decimal

from .utils import compress



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
    
    def get_signature(self):
        return self.doc_name.replace(" ", "")

    
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
    picture = models.FileField(upload_to='patient_pictures', default='default-img.jpg')
    pass_text = models.CharField(max_length=130, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Patients"
        verbose_name_plural = "Patients"
        ordering = ('-created',)

    def __str__(self):
        return self.full_name
    
    def get_signature(self):
        name = self.full_name.replace(" ", "")
        doctor = self.full_name.replace("Dr", "")
        return f'{doctor}{name}' 



class Billing(models.Model):

    Currency = (
        ("$", "USD"),
        ("£", "Pounds"),
        ("€", "Euro"),
    )


    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    report_summary = models.TextField(null=True, blank=True)
    days_spent = models.IntegerField(null=True, blank=True)
    billing_date = models.DateField()
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    billing_receipt = models.CharField(max_length=30, null=True, blank=True)
    currency = models.CharField(max_length=10, choices=Currency)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)


    def __str__(self):
        return self.patient.full_name
    
    def save(self, *args, **kwargs):
        if self.billing_receipt == '' or self.billing_receipt == None:
            num = random.randint(0000000, 9999999)
            num2 = random.randint(000, 999)
            self.billing_receipt = f'{num}-CMCEJ{num2}'
        super(Billing, self).save(*args, **kwargs)
    

    def get_balance(self):
        discount = math.floor((self.bill_amount * Decimal(0.98)) / 100)
        all_deduct = self.paid_amount + discount + 100
        balance = self.bill_amount - all_deduct
        return balance

    def get_discount(self):
        return math.floor((self.bill_amount * Decimal(0.98)) / 100)
    

class BillingSpecification(models.Model):
    spec_name = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.spec_name
    

class BillingItem(models.Model):
    billing = models.ForeignKey(Billing, related_name='billing_items', on_delete=models.CASCADE, null=True, blank=True)
    billing_specification = models.ForeignKey(BillingSpecification, related_name='billing_item', on_delete=models.CASCADE)
    bill_value = models.CharField(max_length=30, null=True, blank=True)
    bill_qty = models.CharField(max_length=30, default=1)

    def __str__(self):
        return self.billing_specification.spec_name
    
    def get_single_total(self, *args, **kwargs):
        return int(self.bill_value) * int(self.bill_qty)
    

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, related_name='prescription', on_delete=models.CASCADE)
    cash_manager = models.CharField(max_length=150)
    hospital = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.patient.full_name
    

class Payment(models.Model):
    billing = models.ForeignKey(Billing, related_name='payment', on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, related_name='payment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt = models.FileField(upload_to='payement_receipts', null=True, blank=True)
    payment_summary = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)


    def save(self, *args, **kwargs):
        new_image = compress(self.receipt)
        self.receipt = new_image
        super().save(*args, **kwargs)

    def __str__(self):
        return self.patient.full_name
    

class Apointment(models.Model):
    patient = models.ForeignKey(Patient, related_name='appointment', on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.full_name


class Address(models.Model):
    address_name = models.CharField(max_length=300)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.address_name


