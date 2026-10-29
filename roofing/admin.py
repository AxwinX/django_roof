from django.contrib import admin
from .models import Product, Appointment, Enquiry, Service


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'is_active', 'created_at', 'updated_at')
    list_filter = ('product_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'date', 'time', 'service', 'status', 'created_at')
    list_filter = ('status', 'service', 'date', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'city')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
    ordering = ('-created_at',)


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'price', 'is_active', 'created_at', 'updated_at')
    list_filter = ('service_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')