from django.db import models


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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