from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator
from .models import Product, Appointment, Enquiry, Service, Profile
from .forms import AppointmentForm, ProductForm, EnquiryForm, ServiceForm, ProfileImageForm
from django.views.decorators.http import require_POST
from django.db.models import Q
from .pagination import paginate


def home(request):
    products = Product.objects.filter(is_active=True)
    services = Service.objects.filter(is_active=True)

    # Handle appointment form
    if request.method == 'POST':
        if 'appointment_submit' in request.POST:
            appointment_form = AppointmentForm(request.POST)
            if appointment_form.is_valid():
                appointment_form.save()
                messages.success(request, "Appointment booked! We'll get back to you within 24 hours.")
                return redirect('home')
        elif 'enquiry_submit' in request.POST:
            enquiry_form = EnquiryForm(request.POST)
            if enquiry_form.is_valid():
                enquiry_form.save()
                messages.success(request, "Your enquiry has been submitted! We'll respond within 24 hours.")
                return redirect('home')
    else:
        appointment_form = AppointmentForm()
        enquiry_form = EnquiryForm()

    return render(request, 'index.html', {
        'products': products,
        'services': services,
        'appointment_form': appointment_form,
        'enquiry_form': enquiry_form,
    })


def staff_required(user):
    return user.is_staff and user.is_authenticated



@user_passes_test(staff_required)
def dashboard(request):
    return render(request, 'dashboard.html', {
        'appointment_total': Appointment.objects.count(),
        'appointment_pending': Appointment.objects.filter(status='pending').count(),
        'enquiry_total': Enquiry.objects.count(),
        'enquiry_pending': Enquiry.objects.filter(status='pending').count(),
        'product_total': Product.objects.count(),
        'product_active': Product.objects.filter(is_active=True).count(),
        'service_total': Service.objects.count(),
        'service_active': Service.objects.filter(is_active=True).count(),
        'recent_appointments': Appointment.objects.order_by('-created_at', '-pk')[:5],
        'recent_enquiries': Enquiry.objects.order_by('-created_at', '-pk')[:5],
    })
    
# =============================
# Product Management (Staff Only)
# =============================

@user_passes_test(staff_required)
def product_list(request):
    products = Product.objects.all().order_by('-created_at', '-pk')
    return render(request, 'product_list.html', paginate(request, products, 9))


@user_passes_test(staff_required)
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully!")
            return redirect('product_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form, "title": "Add Product"})


@user_passes_test(staff_required)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('product_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form, "title": "Edit Product"})


@user_passes_test(staff_required)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("product_list")
    return render(request, "product_confirm_deletion.html", {
        "product": product
    })



# Appointment Management


@user_passes_test(staff_required)
def appointment_list(request):
    appointments = Appointment.objects.all().order_by('-created_at', '-pk')

    status_filter = request.GET.get('status', '').strip()
    if status_filter in dict(Appointment.STATUS_CHOICES):
        appointments = appointments.filter(status=status_filter)
    else:
        status_filter = ''

    search = request.GET.get('search', '').strip()
    if search:
        appointments = appointments.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
        )

    context = paginate(request, appointments, 10)
    context.update({
        'status_choices': Appointment.STATUS_CHOICES,
        'current_status': status_filter,
        'search_query': search,
    })
    return render(request, 'appointment_list.html', context)


@user_passes_test(staff_required)
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointment_detail.html', {'appointment': appointment})


@user_passes_test(staff_required)
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        # Update status only
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            messages.success(request, f"Appointment status updated to {new_status}.")
        return redirect('appointment_list')
    return render(request, 'appointment_update.html', {
        'appointment': appointment,
        'status_choices': Appointment.STATUS_CHOICES,
    })


@user_passes_test(staff_required)
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appointment.delete()
        messages.success(request, "Appointment deleted successfully!")
        return redirect("appointment_list")
    return render(request, "appointment_confirm_deletion.html", {
        "appointment": appointment
    })



# Enquiry Management (Staff)


@user_passes_test(staff_required)
def enquiry_list(request):
    enquiries = Enquiry.objects.all().order_by('-created_at', '-pk')

    status_filter = request.GET.get('status', '').strip()
    if status_filter in dict(Enquiry.STATUS_CHOICES):
        enquiries = enquiries.filter(status=status_filter)
    else:
        status_filter = ''

    search = request.GET.get('search', '').strip()
    if search:
        enquiries = enquiries.filter(
            Q(name__icontains=search)
            | Q(email__icontains=search)
            | Q(subject__icontains=search)
        )

    context = paginate(request, enquiries, 10)
    context.update({
        'status_choices': Enquiry.STATUS_CHOICES,
        'current_status': status_filter,
        'search_query': search,
    })
    return render(request, 'enquiry_list.html', context)


@user_passes_test(staff_required)
def enquiry_detail(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    return render(request, 'enquiry_detail.html', {'enquiry': enquiry})


@user_passes_test(staff_required)
def enquiry_update(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    if request.method == "POST":
        form = EnquiryForm(request.POST, instance=enquiry)
        if form.is_valid():
            form.save()
            messages.success(request, "Enquiry updated successfully!")
            return redirect('enquiry_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EnquiryForm(instance=enquiry)
    return render(request, 'enquiry_form.html', {
        'form': form,
        'enquiry': enquiry,
        'title': "Update Enquiry"
    })


@user_passes_test(staff_required)
def enquiry_delete(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    if request.method == "POST":
        enquiry.delete()
        messages.success(request, "Enquiry deleted successfully!")
        return redirect("enquiry_list")
    return render(request, "enquiry_confirm_deletion.html", {
        "enquiry": enquiry
    })


# Service operations

@user_passes_test(staff_required)
def service_list(request):
    services = Service.objects.all().order_by('-created_at', '-pk')
    return render(request, 'service_list.html', paginate(request, services, 9))


@user_passes_test(staff_required)
def service_create(request):
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service created successfully!")
            return redirect('service_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ServiceForm()
    return render(request, 'service_form.html', {'form': form, "title": "Add Service"})


@user_passes_test(staff_required)
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully!")
            return redirect('service_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ServiceForm(instance=service)
    return render(request, 'service_form.html', {'form': form, "title": "Edit Service"})


@user_passes_test(staff_required)
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        service.delete()
        messages.success(request, "Service deleted successfully!")
        return redirect("service_list")
    return render(request, "service_confirm_deletion.html", {
        "service": service
    })



def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome to SS India Roofing.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')


# Profile Management

@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile image updated successfully!")
            return redirect("profile")
        # validation errors are shown inline by the template
    else:
        form = ProfileImageForm(instance=profile)

    return render(request, "profile.html", {"form": form, "profile": profile})


@login_required
@require_POST
def profile_image_delete(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if profile.image:
        profile.delete_image_file()
        profile.save()
        messages.success(request, "Profile image removed.")
    else:
        messages.info(request, "You don't have a profile image to remove.")
    return redirect("profile")