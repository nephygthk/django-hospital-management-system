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
    # path('<pk>/update_patient/', views.UpdatePatientView.as_view(), name='update_patient'),
    path('<pk>/delete_patient/', views.delete_patient_account, name='delete_patient'),
    path('add_doctor/', views.AddAndViewDoctorView.as_view(), name='add_doctor'),
    path('add_billing/', views.AddBillingView.as_view(), name='add_billing'),

    # patient urls
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard')
]
