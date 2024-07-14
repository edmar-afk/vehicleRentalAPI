from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_num = models.TextField()
    profile_pic = models.FileField(
        upload_to='media/',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])],
    )
    
    def __str__(self):
        return self.user.first_name

class Rental(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_name = models.TextField()
    description = models.TextField()
    images = models.FileField(upload_to='media/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])],)
    location = models.TextField()
    price = models.IntegerField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.vehicle_name