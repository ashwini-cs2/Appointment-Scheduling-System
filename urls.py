from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.staff_list, name='staff_list'),
    path('add/', views.add_staff, name='add_staff'),
    path('<int:pk>/', views.staff_detail, name='staff_detail'),
    path('<int:pk>/edit/', views.edit_staff, name='edit_staff'),
    path('<int:pk>/delete/', views.delete_staff, name='delete_staff'),
    path('<int:staff_pk>/services/', views.manage_services, name='manage_services'),
    path('<int:staff_pk>/services/<int:service_pk>/delete/', views.delete_service, name='delete_service'),
]
