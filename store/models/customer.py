from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    phone_number = models.CharField(max_length = 15)
    email = models.EmailField()
    password = models.CharField(max_length = 500)

    def register(self):
        self.save()

    def isExist(self):
       if Customer.objects.filter(email = self.email):
           return True

       return False