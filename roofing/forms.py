from django import forms
from .models import Appointment, Product


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
        fields = ["name", "description", "image"]
