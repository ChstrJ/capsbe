from django.urls import path
from .views.resident_view import get_residents, find_resident, paginate_residents, create_resident, delete_resident, update_resident

urlpatterns = [
    path('residents/', get_residents, name='get_residents'),
    path("residents/create", create_resident, name="create_resident"),
    path("residents/<uuid:pk>/", find_resident, name="find_resident"),
    path("residents/<uuid:pk>/delete", delete_resident, name="delete_resident"),
    path("residents/<uuid:pk>/update", update_resident, name="update_resident"),
    path("residents-paginate", paginate_residents, name="paginate_residents")
]