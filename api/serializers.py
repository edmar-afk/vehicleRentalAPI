from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Rental, Profile, Favorites, ChatRoom, Message, RentalLike, RateOwner, RateCustomer

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



class RentalLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalLike
        fields = ['id', 'user', 'rental']
        extra_kwargs = {
            'user': {'read_only': True},  # User will be set programmatically
        }



class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)  # Include profile data

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']
        
   
class DisplayRentalSerializer(serializers.ModelSerializer):
    posted_by = UserProfileSerializer()

    class Meta:
        model = Rental
        fields = ['id', 'posted_by', 'description', 'images', 'location', 'date_posted']
        extra_kwargs = {'posted_by': {'read_only': True}}
        
        
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user', 'mobile_num', 'profile_pic']  # Ensure this matches your model fields


class FavoritesSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Favorites
        fields = ['post']
        
class UserFavoriteSerializer(serializers.ModelSerializer):
    post = DisplayRentalSerializer()
    user_profile = ProfileSerializer(source='user.profile')

    class Meta:
        model = Favorites
        fields = ['id', 'post', 'user_profile']

    def get_post(self, obj):
        # Serialize the related post
        from .serializers import RentalSerializer
        return RentalSerializer(obj.post).data
    
    

        
        
class UserRentalListSerializer(serializers.ModelSerializer):
    posted_by = UserSerializer()
    class Meta:
        model = Rental
        fields = ['id','posted_by', 'description', 'images', 'location', 'date_posted']
        
class RentalDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'

    def validate_id(self, value):
        if not Rental.objects.filter(id=value).exists():
            raise serializers.ValidationError("Rental with this ID does not exist.")
        return value
    
class RentalLikeSerializer(serializers.ModelSerializer):
    # Optionally, include the related user and rental as nested fields
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    rental = serializers.PrimaryKeyRelatedField(queryset=Rental.objects.all())

    class Meta:
        model = RentalLike
        fields = ['id', 'user', 'rental']

    def validate(self, data):
        # Ensure a user can only like a rental once
        if RentalLike.objects.filter(rental=data['rental'], user=data['user']).exists():
            raise serializers.ValidationError("This user has already liked this rental.")
        return data  



class ChatRoomSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'users']  # Include 'users' field to show associated users

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    chat_room = serializers.PrimaryKeyRelatedField(queryset=ChatRoom.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'chat_room', 'sender', 'content', 'timestamp']
        


class RateOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateOwner
        fields = ['id', 'owner', 'rate_by', 'points']
        

class RateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateCustomer
        fields = ['id', 'customer', 'rate_by', 'points']
