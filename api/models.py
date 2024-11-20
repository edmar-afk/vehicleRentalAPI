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
    
    
class RentalLike(models.Model):
    rental = models.ForeignKey(Rental, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('rental', 'user')  # Ensures a user can only like a rental once

    def __str__(self):
        return f'{self.user} liked {self.rental}'    
    

class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Rental, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  

    class Meta:
        unique_together = ('user', 'post')
    

class Like(models.Model):
    renter = models.ForeignKey(Rental, on_delete=models.CASCADE)

class ChatRoom(models.Model):
    users = models.ManyToManyField(User, related_name='chat_rooms')

    def __str__(self):
        return f'Chat Room with users: {", ".join(user.username for user in self.users.all())}'

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username}: {self.content}'
    
    
class RateOwner(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rates_received')
    rate_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rates_given')
    points = models.IntegerField()  # IntegerField is more appropriate for numeric ratings

    def __str__(self):
        return f'{self.rate_by} rated {self.owner} {self.points} points'
    
class RateCustomer(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_rates_received')
    rate_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_rates_given')
    points = models.IntegerField()  # IntegerField is more appropriate for numeric ratings

    def __str__(self):
        return f'{self.rate_by} rated {self.customer} {self.points} points'