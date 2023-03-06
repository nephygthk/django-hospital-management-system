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
    

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"
        

    def __str__(self):
        return self.email
    
class Patient(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    patient_id = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=20)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    admission_date = models.DateField()
    discharge_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Patients"
        verbose_name_plural = "Patients"
        ordering = ('-created',)

    def __str__(self):
        return self.full_name

