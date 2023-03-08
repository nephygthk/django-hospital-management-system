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

    # patient urls
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard')
]
