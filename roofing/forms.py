from django import forms
from .models import Appointment, Product, Enquiry, Service, Profile


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
        
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={"accept": "image/jpeg,image/png,image/webp", "id": "id_image"}
            )
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            raise forms.ValidationError("Please choose an image to upload.")
        return image