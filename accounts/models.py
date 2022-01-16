from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    role_choices = [
        ("Admin","Admin"),
        ("Manager","Manager"),
        ("Customer","Customer"),
    ] 
    role = models.CharField(choices= role_choices,default="Customer", max_length=9)
    email = models.EmailField(unique=True,  null = True, blank = True)
    device = models.CharField(max_length=50, null = True, blank = True)

    
class Admin(CustomUser):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.id :
            self.is_superuser = True
        super(Admin, self).save(*args, **kwargs)    

          
class Manager(CustomUser):
    class Meta:
        proxy = True
    def save(self, *args, **kwargs):
        if not self.id :
            self.is_superuser = False
            self.is_staff = True
        super(Manager, self).save(*args, **kwargs) 

class Customer(CustomUser):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.id :
            self.is_superuser = False
            self.is_staff = False
        super(Customer, self).save(*args, **kwargs) 
       

