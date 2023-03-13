from django import forms
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)

from .models import (Billing, BillingItem, BillingSpecification,
            Customer, Doctor, Patient, Payment, Prescription)


class DateInput(forms.DateInput):
	input_type = 'date'


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['full_name','patient_id','gender', 'date_of_birth', 'blood_group','address',
                  'phone_number', 'admission_date','discharge_date','doctor','picture', 'pass_text']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['pass_text'].widget = forms.HiddenInput()
        self.fields['date_of_birth'].widget = DateInput()
        self.fields['admission_date'].widget = DateInput()
        self.fields['discharge_date'].widget = DateInput()

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)
    
    class Meta:
        model = Customer
        fields = ('email',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'A user with this email already exist, please try another email')
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})
        

class AddDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        exclude = ['created']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class BillingForm(forms.ModelForm):
    report_summary = forms.CharField(
        label='Report Summary', widget=forms.Textarea(attrs={'rows':4, 'cols':15}),)

    class Meta:
        model = Billing
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['billing_date'].widget = DateInput()

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class BillSpecificationForm(forms.ModelForm):
    class Meta:
        model = BillingSpecification
        fields = '__all__'
        exclude = ['created']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})



class BillingItemForm(forms.ModelForm):
    class Meta:
        model = BillingItem
        fields = '__all__'
        exclude = ['billing']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     for field in self.fields:
    #         self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomerUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    
    class Meta:
        model = Customer
        fields = ['email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'id': 'id_email'})
        

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'
        exclude = ['created']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        exclude = ['date_created', 'date_updated', 'patient']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})



class UploadImageForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['full_name','picture']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


BillingItemFormSet = formset_factory(
    BillingItemForm,
    extra=0,
)

EditBillingItemFormSet = modelformset_factory(
    BillingItem,
    BillingItemForm,
    extra=0,
)













    # class SinglePostByCategory(DetailView):
    # def get_queryset(self):
    #     return get_object_or_404(Post,
    #         category__slug=self.kwargs['category_slug'],
    #         slug=self.kwargs['post_slug']