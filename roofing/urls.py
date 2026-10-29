from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
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
]