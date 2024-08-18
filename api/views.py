# views.py
from rest_framework import generics, permissions, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserSerializer, RentalDeleteSerializer, RentalSerializer, ProfileSerializer, FavoritesSerializer,ChatReceiverSerializer, UserRentalListSerializer, DisplayRentalSerializer, UserFavoriteSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Rental, Profile, Favorites
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        username = validated_data.get('username')
        email = validated_data.get('email')
        mobile_num = validated_data.get('mobile_num', None)

        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': 'A user with this username already exists.'})

        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'A user with this email already exists.'})

        if mobile_num and Profile.objects.filter(mobile_num=mobile_num).exists():
            raise ValidationError({'mobile_num': 'A user with this mobile number already exists.'})


        serializer.save()

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    
class RentalSet(generics.CreateAPIView):
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Rental.objects.filter(posted_by=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(posted_by=self.request.user)
        else:
            print(serializer.errors)

class RentalDelete(generics.DestroyAPIView):
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Rental.objects.filter(posted_by=user)
    
    
class RentalListAPIView(generics.ListAPIView):
    queryset = Rental.objects.all().order_by('-id')
    serializer_class = DisplayRentalSerializer
    permission_classes = [permissions.AllowAny]  # Or use permissions.IsAuthenticated if you want only logged-in users to see the rentals    

    def get(self, request, *args, **kwargs):
        # Debugging output
        print(f"Request method: {request.method}")
        response = super().get(request, *args, **kwargs)
        print(f"Response status code: {response.status_code}")
        return response

class ProfilePictureUpdateView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if 'profile_pic' not in request.FILES:
            return Response({'detail': 'No profile picture uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)

        if not created and profile.profile_pic:
            profile.profile_pic.delete(save=False)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
       
        profile = Profile.objects.get(user__id=user_id)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
        
class CreateFavoriteView(generics.CreateAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the user to the currently authenticated user
        serializer.save(user=self.request.user)
        
class UserFavoritesListAPIView(generics.ListAPIView):
    serializer_class = UserFavoriteSerializer

    def get_queryset(self):
        user = self.request.user
        return Favorites.objects.filter(user=user)
    
class ReceiverDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ChatReceiverSerializer

    def get_object(self):
        userid = self.kwargs.get('userid')  # Retrieve userid from URL parameters
        profile = get_object_or_404(Profile, user__id=userid)  # Filter profile based on userid
        return profile
    
    
class UserRentalsView(generics.GenericAPIView):
    serializer_class = UserRentalListSerializer

    def get(self, request, user_id, *args, **kwargs):
        try:
            rentals = Rental.objects.filter(posted_by_id=user_id)
            serializer = self.get_serializer(rentals, many=True)
            return Response(serializer.data)
        except Rental.DoesNotExist:
            raise NotFound("Rentals not found for this user.")
        
class RentalDeleteAPIView(generics.DestroyAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalDeleteSerializer
    lookup_field = 'id'