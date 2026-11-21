from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Product Management
    path("manage/products/", views.product_list, name="product_list"),
    path("manage/products/add/", views.product_create, name="product_create"),
    path(
        "manage/products/edit/<int:pk>/",
        views.product_update,
        name="product_update"
    ),
    path(
        "manage/products/delete/<int:pk>/",
        views.product_delete,
        name="product_delete"
    ),

    # Appointment Management
    path("manage/appointments/", views.appointment_list, name="appointment_list"),
    path(
        "manage/appointments/<int:pk>/",
        views.appointment_detail,
        name="appointment_detail"
    ),
    path(
        "manage/appointments/<int:pk>/edit/",
        views.appointment_update,
        name="appointment_update"
    ),
    path(
        "manage/appointments/<int:pk>/delete/",
        views.appointment_delete,
        name="appointment_delete"
    ),

    # Enquiry Management
    path("manage/enquiries/", views.enquiry_list, name="enquiry_list"),
    path(
        "manage/enquiries/<int:pk>/",
        views.enquiry_detail,
        name="enquiry_detail"
    ),
    path(
        "manage/enquiries/<int:pk>/edit/",
        views.enquiry_update,
        name="enquiry_update"
    ),
    path(
        "manage/enquiries/<int:pk>/delete/",
        views.enquiry_delete,
        name="enquiry_delete"
    ),
    
    path("manage/", views.dashboard, name="dashboard"),
    

    # Service Management
    path("manage/services/", views.service_list, name="service_list"),
    path("manage/services/add/", views.service_create, name="service_create"),
    path(
        "manage/services/edit/<int:pk>/",
        views.service_update,
        name="service_update"
    ),
    path(
        "manage/services/delete/<int:pk>/",
        views.service_delete,
        name="service_delete"
    ),
    
    # Profile Management
    path('profile/', views.profile_view, name='profile'),
    path('profile/image/delete/', views.profile_image_delete, name='profile_image_delete'),

]