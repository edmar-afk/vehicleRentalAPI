from django.contrib import admin
from .models import Profile, Favorites, Rental, ChatRoom, Message, RateOwner
# Register your models here.


admin.site.register(Profile)
admin.site.register(Rental)
admin.site.register(Favorites)
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(RateOwner)
