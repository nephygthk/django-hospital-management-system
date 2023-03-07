from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.models import modelform_factory

from .models import Billing, BillingSpecification, Customer, Doctor, Patient
from .forms import (AddDoctorForm, BillSpecificationForm,
            BillingForm, BillingItemForm, RegistrationForm, PatientForm)

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
            
            messages.success(
                self.request,
                    f'Patient created successfully '
                    )

            return HttpResponseRedirect(
                reverse_lazy('account:all_patient')
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
    

class AllPatientView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'account/admin/patient.html'
    context_object_name = 'patients'
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponse("Error handler content", status=400)
        return super().dispatch(request, *args, **kwargs)
    

# class UpdatePatientView(UpdateView):
#     model = Customer
#     form_class  = CustomerUpdateForm
#     second_form_class = PatientForm
#     template_name = "account/admin/update_patient.html"

#     def dispatch(self, request, *args, **kwargs):
#         if not self.request.user.is_staff:
#             return HttpResponse("Error handler content", status=400)
#         return super().dispatch(request, *args, **kwargs)
    
#     def get_context_data(self, **kwargs):
#         kwargs['active_client'] = True
#         if 'form' not in kwargs:
#             kwargs['form'] = self.form_class(instance=self.get_object())
#         if 'form2' not in kwargs:
#             kwargs['form2'] = self.second_form_class(instance=self.get_object().patient) 
#         return super(UpdatePatientView, self).get_context_data(**kwargs)
    
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.form_class(request.POST)
#         form2 = self.second_form_class(request.POST)

#         if form.is_valid() and form2.is_valid():
#             form.save()
#             form2.save()
#             messages.success(self.request, 'Patient Updated successfully')
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return self.render_to_response(
#               self.get_context_data(form=form, form2=form2))
        
#     def get_success_url(self):
#         return reverse_lazy('account:admin_dashboard')


def delete_patient_account(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    customer.delete()
    messages.success(request, 'Patient deleted successfully')
    return redirect('account:admin_dashboard')


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
    

def delete_doctor(request, pk):
    doctor = get_object_or_404(Doctor, id=pk)
    doctor.delete()
    messages.success(request, 'Doctor deleted successfully')
    return redirect('account:add_doctor')
    

class AddBillingView(TemplateView):
    model = Billing
    form_class = BillingForm
    template_name = 'account/admin/add_billing.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponse("Error handler content", status=400)
        return super().dispatch(request, *args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
        billing_form = BillingForm(self.request.POST)
        bill_item_form = BillingItemForm(self.request.POST)

        if billing_form.is_valid() and bill_item_form.is_valid():
            billingme = billing_form.save()
            billingus = bill_item_form.save(commit=False)
            billingus.billing = billingme
            billingus.save()

            messages.success(
                self.request,
                f'Bill added successfully'
            )

            return HttpResponseRedirect(
                    reverse_lazy('account:all_billing')
                )
        print('not valid')
        return self.render_to_response(
            self.get_context_data(
                billing_form=billing_form,
                bill_item_form=bill_item_form,
            )
        )
    
    def get_context_data(self, **kwargs):
        if 'billing_form' not in kwargs:
            kwargs['billing_form'] = BillingForm()
        if 'bill_item_form' not in kwargs:
            kwargs['bill_item_form'] = BillingItemForm()
        return super().get_context_data(**kwargs)



class AllBillingsView(LoginRequiredMixin, ListView):
    model = Billing
    template_name = 'account/admin/billings.html'
    context_object_name = 'billings'
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponse("Error handler content", status=400)
        return super().dispatch(request, *args, **kwargs)	
    

def delete_billing(request, pk):
    billing = get_object_or_404(Billing, id=pk)
    billing.delete()
    messages.success(request, 'Billing deleted successfully')
    return redirect('account:add_billing')
    
class AddBillSpecificationView(LoginRequiredMixin, CreateView):
    model = BillingSpecification
    form_class = BillSpecificationForm
    template_name = "account/admin/add_bill_specification.html"
    success_url = reverse_lazy('account:add_billing_specification')

    def get_context_data(self, **kwargs):
       context = super(AddBillSpecificationView, self).get_context_data(**kwargs)
       context['bill_specs'] = BillingSpecification.objects.all()
       return context



@login_required
def patient_dashboard(request):
    return render(request, 'account/patient/p_dashboard.html', {})