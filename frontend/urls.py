from django.urls import path

from . import views

app_name = "frontend"

urlpatterns = [
    path('',views.Home.as_view(), name='home'),
    path('contact/',views.Contact.as_view(), name='contact'),
]