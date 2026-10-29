from django import forms
from .models import Appointment, Product, Enquiry, Service


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = [
            'first_name',
            'last_name',
            'city',
            'phone',
            'email',
            'date',
            'time',
            'service',
            'message',
        ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "product_type", "is_active"]


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'service_type', 'description', 'image', 'is_active', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
