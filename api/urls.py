from django.urls import path
from .views.resident_view import (
    GetResidentsView,
    PaginateResidentsView,
    FindResidentView,
    CreateResidentView,
    DeleteResidentView,
    UpdateResidentView,
)

from .views.auth_view import (
    LoginView,
    AdminRegisterView,
    ResidentRegisterView
)

from .views.department_view import (
    GetDepartmentsView,
    GenerateDepartmentsView,
    GetAvailableCountView,
    CreateDepartmentView,
    DeleteDepartmentView,
    UpdateDepartmentView
)

from .views.alert_view import (
    CreateAlertView,
    SendSmsView,
    SendEmailView
)

urlpatterns = [
    path('residents', GetResidentsView.as_view(), name='get-residents'),
    path('residents/paginate', PaginateResidentsView.as_view(), name='paginate-residents'),
    path('residents/<uuid:pk>', FindResidentView.as_view(), name='find-resident'),
    path('residents/create', CreateResidentView.as_view(), name='create-resident'),
    path('residents/delete/<uuid:pk>', DeleteResidentView.as_view(), name='delete-resident'),
    path('residents/update/<uuid:pk>', UpdateResidentView.as_view(), name='update-resident'),
    
    path('auth/login', LoginView.as_view(), name='admin-login'),
    path('auth/register/admin', AdminRegisterView.as_view(), name='admin-register'),
    path('auth/register/resident', ResidentRegisterView.as_view(), name='resident-register'),
    
    path('departments', GetDepartmentsView.as_view(), name='get-departments'),
    path('departments/generate', GenerateDepartmentsView.as_view(), name='generate-departments'),
    path('departments/create', CreateDepartmentView.as_view(), name='create-department'),
    path('departments/delete/uuid:pk', DeleteDepartmentView.as_view(), name='delete-department'),
    path('departments/update/uuid:pk', UpdateDepartmentView.as_view(), name='update-department'),
    path('departments/available', GetAvailableCountView.as_view(), name='get-available'),
    
    path('send/alert', CreateAlertView.as_view(), name='send-alert'),
    path('send-sms/fire', SendSmsView.as_view(), name='send-sms'),
    path('send-sms/police', SendSmsView.as_view(), name='send-sms'),
    path('send-sms/medical', SendSmsView.as_view(), name='send-sms'),
    
    path('send-email', SendEmailView.as_view(), name='send-sms'),
]
