from itertools import count
from django.shortcuts import render, redirect
from django.http import HttpResponse
from RealTime_Data_Analystics import models
from .models import Product
import statistics
import json
from scipy import stats
import numpy as np
from django.db.models import Avg, Max, Min, Count,Sum

def dash_board(request):
    
    return render(request, 'dashboard.html')

def submit_form(request):
    if request.method == 'POST':
        try:
            product_id = int(request.POST.get('productId', 0))
            product_name = request.POST.get('productName', '')
            product_category = request.POST.get('category', '')
            sales_price = float(request.POST.get('salesAmount', 0.0))
            unit_sold = float(request.POST.get('unitsSold', 0.0))
            region = request.POST.get('region', '')
            customer_age = int(request.POST.get('customerAge', 0))

            # Create and save a single Product
            new_product = models.Product(
                ProductID=product_id,
                ProductName=product_name,
                ProductCategory=product_category,
                SalesAmount=sales_price,
                UnitSold=unit_sold,
                Region=region,
                Age=customer_age
            )
            new_product.save()
        except ValueError as e:
            # Handle the case where type conversion fails
            return HttpResponse(f"Error processing form data: {e}")
        except Exception as e:
            # Handle other possible exceptions
            return HttpResponse(f"An unexpected error occurred: {e}")

        return HttpResponse('Successfully Entered the data...!')  # Replace 'success_url' with your success page URL or name
    else:
        return render(request, 'index.html')


def show_products(request):
    # Fetch all products from the database
    products = Product.objects.all()

    # Pass the products to the template
    return render(request, 'products.html', {'products': products})

def insight_products(request):
    # Fetch all products
    products = Product.objects.all()
    
    # Initialize lists for data
    sales_data = list(products.values_list('SalesAmount', flat=True))
    units_data = list(products.values_list('UnitSold', flat=True))
    ages_data = list(products.values_list('Age', flat=True))
    
    # Default values
    sales_mean = sales_median = sales_mode = 0
    units_mean = units_median = units_mode = 0
    ages_mean = ages_median = ages_mode = 0
    
    # Calculate mean, median, and mode only if data is available
    if sales_data:
        sales_mean = np.mean(sales_data)
        sales_median = np.median(sales_data)
        try:
            sales_mode_result = stats.mode(sales_data)
            sales_mode = sales_mode_result[0]
        except IndexError:
            sales_mode = 0
    
    if units_data:
        units_mean = np.mean(units_data)
        units_median = np.median(units_data)
        try:
            units_mode_result = stats.mode(units_data)
            units_mode = units_mode_result[0]
        except IndexError:
            units_mode = 0
    
    if ages_data:
        ages_mean = np.mean(ages_data)
        ages_median = np.median(ages_data)
        try:
            ages_mode_result = stats.mode(ages_data)
            ages_mode = ages_mode_result[0]
        except IndexError:
            ages_mode = 0
    
    # Pie chart data for product categories
    category_data = list(products.values('ProductCategory').annotate(total=Count('ProductCategory')))
    category_labels = [item['ProductCategory'] for item in category_data]
    category_counts = [item['total'] for item in category_data]
    
    # Remove time-based analysis if 'SaleDate' field does not exist
    context = {
        'sales_mean': sales_mean,
        'sales_median': sales_median,
        'sales_mode': sales_mode,
        'units_mean': units_mean,
        'units_median': units_median,
        'units_mode': units_mode,
        'ages_mean': ages_mean,
        'ages_median': ages_median,
        'ages_mode': ages_mode,
        'sales_data': sales_data,
        'units_data': units_data,
        'ages_data': ages_data,
        'labels': list(range(1, len(sales_data) + 1)),  # Assuming labels are sequential
        'category_labels': category_labels,
        'category_data': category_counts,
    }
    
    return render(request, 'products_insights.html', context)