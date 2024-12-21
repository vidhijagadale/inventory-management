from django.contrib import admin
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import Sale
from .models import Vendor
from .models import Customer

import re

class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'Customer', 'qty', 'price', 'total_amt', 'sale_date']

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()  # Triggers the `clean` method in the model
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(request, f"Error: {e}", level="error")

admin.site.register(Sale, SaleAdmin)



def validate_email_format(email):
    """Validate the email address format."""
    if ' ' in email:
        raise ValidationError('Email address should not contain spaces.')
    if not email.endswith('@gmail.com'):
        raise ValidationError('Email address must end with @gmail.com.')

def create_vendor(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email_address = request.POST.get('email_address', '').strip()
        address = request.POST.get('address', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        status = request.POST.get('status') == 'on'  # Checkbox handling

        # Validation logic for email
        try:
            validate_email_format(email_address)

            # Save the vendor if validation passes
            vendor = Vendor(
                full_name=full_name,
                email_address=email_address,
                address=address,
                mobile=mobile,
                status=status
            )
            vendor.save()
            return JsonResponse({'message': 'Vendor created successfully!'}, status=201)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

    # If the method is not POST, return a bad request response
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def validate_customer_email(email):
    """Validate the email format to exclude spaces and restrict @gmail.com."""
    if ' ' in email:
        raise ValidationError('Email address should not contain spaces.')
    if '@gmail.com' in email:
        raise ValidationError('Email addresses with @gmail.com are not allowed.')

def create_customer(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_mobile = request.POST.get('customer_mobile')
        customer_email = request.POST.get('customer_email')
        customer_address = request.POST.get('customer_address')

        # Email validation
        try:
            validate_customer_email(customer_email)

            # Save the customer if validation passes
            customer = Customer(
                customer_name=customer_name,
                customer_mobile=customer_mobile,
                customer_email=customer_email,
                customer_address=customer_address
            )
            customer.save()
            return JsonResponse({'message': 'Customer created successfully!'}, status=201)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'customer_form.html')