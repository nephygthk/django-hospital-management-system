from django.shortcuts import render
from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = 'frontend/index.html'


class Contact(TemplateView):
    template_name = 'frontend/contact.html'