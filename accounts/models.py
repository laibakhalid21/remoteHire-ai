from django.db import models
from .managers import UserManager
# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        #value and label are same, but the first value is the actual value stored in the database, and the second value is the human-readable name for the choice.
        #all django's model fucntionality charfield,emailfield,textchoices,booleanfield,integerfield,datetimefield,foreignkey,one-to-one field,many-to-many field, 
        Professional='professional','Professional'
        Company='company','Company'

    username=None
    email=models.EmailField(unique=True)
    role=models.CharField(max_length=20,choices=Role.choices)
    is_verified=models.BooleanField(default=False)

    objects=UserManager()
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.email
