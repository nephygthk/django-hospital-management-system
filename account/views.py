from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .models import Customer

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('account:admin_dashboard')
            else:
                login(request, user)
                return redirect('account:patient_dashboard')
    else:
        messages.info(request, 'Username OR password is incorrect')
    return render(request, 'account/login.html', {})


# @login_required
# def admin_dashboard(request):
#     if not request.user.is_staff:
#         return HttpResponse("Error handler content", status=400)
    
#     return render(request, 'account/admin/dashboard.html', {})

class AdminDashboardView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'account/admin/dashboard.html'
    context_object_name = 'customers'
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponse("Error handler content", status=400)
        return super().dispatch(request, *args, **kwargs)	


@login_required
def patient_dashboard(request):
    return render(request, 'account/patient/p_dashboard.html', {})