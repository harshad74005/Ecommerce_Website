# store/models/customer.py

from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=50)
    phno = models.CharField(max_length=15)

    # 🎯 ADD THE NEW EMAIL FIELD HERE
    email = models.EmailField(max_length=100, unique=True, null=True)

    def register(self):
        self.save()

    def isExists(self):
        # We should also check if the email already exists here!
        if Customer.objects.filter(phno=self.phno).exists() or \
                Customer.objects.filter(email=self.email).exists():
            return True
        else:
            return False