from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path('login/', views.login_user, name='login'),
    
    path("logout/", auth_views.LogoutView.as_view(next_page="/account/login/"), name="logout"),

    # admin urls
    path('admin_dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('add_patient/', views.AddPatientView.as_view(), name='add_patient'),
    path('all_patient/', views.AllPatientView.as_view(), name='all_patient'),
    path('<pk>/update_patient/', views.UpdatePatientView, name='update_patient'),
    path('<pk>/delete_patient/', views.delete_patient_account, name='delete_patient'),
    path('add_doctor/', views.AddAndViewDoctorView.as_view(), name='add_doctor'),
    path('<pk>/delete_doctor/', views.delete_doctor, name='delete_doctor'),
    path('all_billings/', views.AllBillingsView.as_view(), name='all_billings'),
    path('add_billing/', views.add_new_billing, name='add_billing'),
    path('<pk>/billing_detail/', views.BillingDetailsView, name='billing_detail'),
    path('<pk>/edit_billing/', views.edit_billing, name='edit_billing'),
    path('<pk>/delete_billing/', views.delete_billing, name='delete_billing'),
    path('add_billing_specification/', views.AddBillSpecificationView.as_view(), name='add_billing_specification'),
    path('<pk>/delete_billing_specification/', views.delete_billing_specification, name='delete_billing_specification'),
    path('payment_list/', views.PaymentListView.as_view(), name='payment_list'),
    path('add_prescription/', views.PrescriptionView.as_view(), name='add_prescription'),
    path('<pk>/upload_image/', views.upload_image, name='upload_image'),
    

    # patient urls
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient_status/', views.patient_status, name='patient_status'),
    path('patient_billing/', views.patient_billing, name='patient_billing'),
    path('make_payment/', views.make_payment, name='make_payment'),
    path('<pk>/delete_payment/', views.delete_payment, name='delete_payment'),
    path('<pk>/view_receipt/', views.view_receipt, name='view_receipt'),

    # pdf
    # path('<pk>/view_billing_pdf/', views.view_billing_pdf, name='view_billing_pdf'),
]
