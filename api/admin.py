from django.contrib import admin
from .models import Profile, Favorites, Rental
# Register your models here.


admin.site.register(Profile)
admin.site.register(Rental)
admin.site.register(Favorites)