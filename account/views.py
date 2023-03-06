from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

from .models import Customer, Doctor
from .forms import AddDoctorForm, RegistrationForm, PatientForm

def login_user(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('account:admin_dashboard')
        else:
            return redirect('account:patient_dashboard')
        
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


class AddPatientView(LoginRequiredMixin, TemplateView):
    model = Customer
    form_class = RegistrationForm
    template_name = 'account/registration/register.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponse("Error handler content", status=400)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        registration_form = RegistrationForm(self.request.POST)
        patient_form = PatientForm(self.request.POST)
        if registration_form.is_valid() and patient_form.is_valid():
            user = registration_form.save(commit=False)
            user.set_password(registration_form.cleaned_data["password"])
            user.save()
            patient = patient_form.save(commit=False)
            patient.customer = user
            patient.save()

            # messages.success(
            #     self.request,
            #         'Patient created successfully '
            #         )

            return HttpResponseRedirect(
                reverse_lazy('account:admin_dashboard')
            )
        
        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                patient_form=patient_form
            )
        )
    
    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = RegistrationForm()
        if 'patient_form' not in kwargs:
            kwargs['patient_form'] = PatientForm()
        return super().get_context_data(**kwargs)


class AdminDashboardView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'account/admin/dashboard.html'
    context_object_name = 'customers'
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponse("Error handler content", status=400)
        return super().dispatch(request, *args, **kwargs)	
    

class AddAndViewDoctorView(LoginRequiredMixin, CreateView):
    form_class = AddDoctorForm
    success_url = reverse_lazy('account:add_doctor')
    template_name = 'account/admin/add_dcotor.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponse("Error handler content", status=400)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        doc_name = form.cleaned_data.get('doc_name')
        messages.success(
            self.request,
            f'Dr {doc_name} was added successfully'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
       context = super(AddAndViewDoctorView, self).get_context_data(**kwargs)
       context['doctors'] = Doctor.objects.all()
       return context


@login_required
def patient_dashboard(request):
    return render(request, 'account/patient/p_dashboard.html', {})