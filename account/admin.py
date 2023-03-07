from django.contrib import admin

from .models import (Customer, Patient, Doctor,
        Billing, BillingSpecification,
        BillingItem)

admin.site.register(Customer)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Billing)
admin.site.register(BillingSpecification)
admin.site.register(BillingItem)