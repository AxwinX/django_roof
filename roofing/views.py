from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Product
from .forms import AppointmentForm, ProductForm


def home(request):
    products = Product.objects.all()

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment booked! We'll get back to you within 24 hours.")
            return redirect('home')
    else:
        form = AppointmentForm()

    return render(request, 'index.html', {
        'products': products,
        'form': form,
    })
    
def staff_required(user):
    return user.is_staff and user.is_authenticated

@user_passes_test(staff_required)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

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
            form = ProductForm()
        return render(request, 'product_create.html', {'form': form, "title": "Add Product"})


@user_passes_test(staff_required)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.isvalid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('product_list')
        else:
            messages.error(request, "Please correct the errors below.")
            form = ProductForm(instance=product)
        return render(request, 'product_update.html', {'form': form, "title": "Edit Product"})
    
@user_passes_test(staff_required)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "product_confirm_deletion.html", {
        "product": product
    })