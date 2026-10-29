from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator
from .models import Product, Appointment, Enquiry, Service
from .forms import AppointmentForm, ProductForm, EnquiryForm, ServiceForm


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


# =============================
# Product Management (Staff Only)
# =============================

@user_passes_test(staff_required)
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product_list.html', {'page_obj': page_obj})


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


# =============================
# Appointment Management (Staff Only)
# =============================

@user_passes_test(staff_required)
def appointment_list(request):
    appointments = Appointment.objects.all().order_by('-created_at')

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        appointments = appointments.filter(status=status_filter)

    # Search
    search = request.GET.get('search')
    if search:
        appointments = appointments.filter(
            first_name__icontains=search
        ) | appointments.filter(
            last_name__icontains=search
        ) | appointments.filter(
            email__icontains=search
        ) | appointments.filter(
            phone__icontains=search
        )

    paginator = Paginator(appointments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'appointment_list.html', {
        'page_obj': page_obj,
        'status_choices': Appointment.STATUS_CHOICES,
        'current_status': status_filter,
        'search_query': search,
    })


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


# =============================
# Enquiry Management (Staff Only)
# =============================

@user_passes_test(staff_required)
def enquiry_list(request):
    enquiries = Enquiry.objects.all().order_by('-created_at')

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        enquiries = enquiries.filter(status=status_filter)

    # Search
    search = request.GET.get('search')
    if search:
        enquiries = enquiries.filter(
            name__icontains=search
        ) | enquiries.filter(
            email__icontains=search
        ) | enquiries.filter(
            subject__icontains=search
        )

    paginator = Paginator(enquiries, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'enquiry_list.html', {
        'page_obj': page_obj,
        'status_choices': Enquiry.STATUS_CHOICES,
        'current_status': status_filter,
        'search_query': search,
    })


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


# =============================
# Service Management (Staff Only)
# =============================

@user_passes_test(staff_required)
def service_list(request):
    services = Service.objects.all().order_by('-created_at')
    paginator = Paginator(services, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'service_list.html', {'page_obj': page_obj})


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