from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.views import View

# Create your views here.
def index(request):
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()
    data = {}
    data['products'] = products
    data['categories'] = categories
    return render(request, 'index.html', data)

def validateCustomer(customer):
    error_message = None
    if not customer.first_name:
        error_message = "Please enter your first name."
    elif not customer.last_name:
        error_message = "Please enter your last name."
    elif not customer.email:
        error_message = "Please enter your email."
    elif not customer.phone_number:
        error_message = "Please enter your phone number."
    elif not customer.password:
        error_message = "Please enter your password."
    elif len(customer.password) < 8:
        error_message = "Password should bo minimum 8 characters."
    elif customer.isExist():
        error_message = 'Account with same email exists.'

    return error_message

def registerUser(request):
    postData = request.POST
    first_name = postData.get('firstname')
    last_name = postData.get('lastname')
    phone_number = postData.get('phonenumber')
    email = postData.get('email')
    password = postData.get('password')
    # validation
    value = {
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number,
        'email': email
    }
    error_message = None
    customer = Customer(first_name=first_name,
                        last_name=last_name,
                        phone_number=phone_number,
                        email=email,
                        password=password)
    error_message = validateCustomer(customer)

    # saving
    if not error_message:
        customer.password = make_password(customer.password)
        customer.register()
        return redirect('homepage')
    else:
        data = {
            "error": error_message,
            "values": value
        }
        return render(request, 'signup.html', data)

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        return registerUser(request)

def login(request):
    if request.method == 'GET':
        return render(request, "login.html")
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                return redirect('homepage')
            else:
                error_message = "Email or Password is invalid!"
        else:
            error_message = "Email or Password is invalid!"
        return render(request, 'login.html', {'error' : error_message})