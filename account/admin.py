from django.contrib import admin

from .models import Customer, Patient, Doctor, Billing

admin.site.register(Customer)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Billing)