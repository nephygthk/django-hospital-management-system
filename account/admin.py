from django.contrib import admin

from .models import Customer, Patient

admin.site.register(Customer)
admin.site.register(Patient)