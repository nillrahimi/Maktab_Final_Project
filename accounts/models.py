from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    
class Admin(CustomUser):
    class Meta:
        proxy = True
          
class Manager(CustomUser):
    class Meta:
        proxy = True

class Customer(CustomUser):
    class Meta:
        proxy = True

