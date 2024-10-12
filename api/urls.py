from django.urls import path
from .views.resident_view import (
    GetResidentsView,
    PaginateResidentsView,
    FindResidentView,
    CreateResidentView,
    DeleteResidentView,
    UpdateResidentView,
)

from .views.admin_view import (
    AdminLoginView,
    AdminRegisterView
)

urlpatterns = [
    # For Mobile App
    path('residents/', GetResidentsView.as_view(), name='get-residents'),
    path('residents/paginate/', PaginateResidentsView.as_view(), name='paginate-residents'),
    path('residents/<uuid:pk>/', FindResidentView.as_view(), name='find-resident'),
    path('residents/create/', CreateResidentView.as_view(), name='create-resident'),
    path('residents/delete/<uuid:pk>/', DeleteResidentView.as_view(), name='delete-resident'),
    path('residents/update/<uuid:pk>/', UpdateResidentView.as_view(), name='update-resident'),
    
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('admin/register/', AdminRegisterView.as_view(), name='admin-register')
]
