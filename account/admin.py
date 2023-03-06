from django.contrib import admin

from .models import Customer, Patient, Doctor

admin.site.register(Customer)
admin.site.register(Patient)
admin.site.register(Doctor)