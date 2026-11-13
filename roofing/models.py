from django.db import models
import os, uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import (
    validate_image_extension, validate_image_size, validate_image_content,
  )
# 

class Product(models.Model):
    PRODUCT_TYPES = [
        ('profile-sheet', 'Profile Sheet'),
        ('linear-sheet', 'Linear Sheet'),
        ('polycarbonate-sheet', 'Polycarbonate Sheet'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField()
    product_type = models.CharField(max_length=30, choices=PRODUCT_TYPES, default='profile-sheet')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('profile-sheet', 'Profile Sheet'),
        ('linear-sheet', 'Linear Sheet'),
        ('polycarbonate-sheet', 'Polycarbonate Sheet'),
        ('installation', 'Installation Service'),
        ('repair', 'Repair Service'),
        ('inspection', 'Roof Inspection'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    service = models.CharField(max_length=30, choices=SERVICE_CHOICES)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.date} {self.time} ({self.status})"


class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('resolved', 'Resolved'),
        ('spam', 'Spam'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.status})"


class Service(models.Model):
    SERVICE_TYPES = [
        ('installation', 'Installation'),
        ('repair', 'Repair'),
        ('maintenance', 'Maintenance'),
        ('inspection', 'Inspection'),
        ('consultation', 'Consultation'),
    ]
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField()
    image = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
def profile_image_path(instance, filename):
    """Store as profile_images/user_<id>/<random>.<ext> so names never clash
    and the original filename is never trusted."""
    ext = os.path.splitext(filename)[1].lower()
    return f"profile_images/user_{instance.user_id}/{uuid.uuid4().hex}{ext}"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    image = models.ImageField(
        upload_to=profile_image_path,
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_image_size, validate_image_content],
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    def delete_image_file(self):
        """Remove the file from disk and clear the field."""
        if self.image:
            self.image.delete(save=False)
            self.image = None

    def save(self, *args, **kwargs):
        # If the image is being replaced, delete the old file from disk.
        if self.pk:
            old = Profile.objects.filter(pk=self.pk).first()
            if old and old.image and old.image != self.image:
                old.image.delete(save=False)
        super().save(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)