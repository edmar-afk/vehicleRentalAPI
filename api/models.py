from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_num = models.TextField()
   
    profile_pic = models.FileField(
        upload_to='profiles/',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])], null=True, blank=True
    )
    
    def __str__(self):
        return self.user.first_name

class Rental(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    images = models.FileField(upload_to='rentals/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])],)
    location = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.posted_by.first_name
    
class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Rental, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Example field

    class Meta:
        unique_together = ('user', 'post')
    

class Message(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    sent_time = models.DateTimeField(auto_now_add=True)  # Default value is the current time
    sender_is_read = models.BooleanField(default=False)
    receiver_is_read = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-sent_time']  # Messages will be ordered by sent time, newest first

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.sent_time}"