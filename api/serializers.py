from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Rental, Profile, Favorites

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_pic']

class UserSerializer(serializers.ModelSerializer):
    mobile_num = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'password', 'mobile_num']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        mobile_num = validated_data.pop('mobile_num')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, mobile_num=mobile_num)
        return user
    
    
class RentalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rental
        fields = ['id', 'posted_by', 'description', 'images', 'location', 'date_posted']
        extra_kwargs = {'posted_by': {'read_only': True}}
        
class DisplayRentalSerializer(serializers.ModelSerializer):
    posted_by = UserSerializer()

    class Meta:
        model = Rental
        fields = ['id', 'posted_by', 'description', 'images', 'location', 'date_posted']
        extra_kwargs = {'posted_by': {'read_only': True}}
        
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'mobile_num', 'profile_pic']  # Ensure this matches your model fields


class FavoritesSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Favorites
        fields = ['post']
        
class UserFavoriteSerializer(serializers.ModelSerializer):
    post = DisplayRentalSerializer()

    class Meta:
        model = Favorites
        fields = ['id', 'post']

    def get_post(self, obj):
        # Serialize the related post
        from .serializers import RentalSerializer
        return RentalSerializer(obj.post).data
    
    
    
class ChatReceiverSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user', 'mobile_num', 'profile_pic'] 