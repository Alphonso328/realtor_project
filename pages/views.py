from django.shortcuts import render
from django.http import HttpResponse
from listings.choices import price_choices, bedroom_choices, state_choices
from listings.models import Listing
from employees.models import Employee

# Create your views here.


def index(request):
    listings =Listing.objects.order_by('-list_date').filter(is_published=True)[:3]

    context = {
        'listings': listings,
        'state_choices': state_choices,
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices
    }
    return render(request, 'pages/index.html', context)


def about(request):
    employees = Employee.objects.order_by('-hire_date')
     
    mvp_employees = Employee.objects.all().filter(is_mvp=True)
    context = {
         'employees': employees,
         'mvp_employees': mvp_employees
     }

    return render(request, 'pages/about.html', context)
