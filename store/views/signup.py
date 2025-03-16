from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View


class SignUp(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        return self.registerUser(request)

    def registerUser(self, request):
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
        error_message = self.validateCustomer(customer)

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

    def validateCustomer(self, customer):
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
