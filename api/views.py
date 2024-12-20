# views.py
from rest_framework import generics, permissions, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserSerializer, ChatRoomSerializer, RateOwnerSerializer, MessageSerializer, CommentsSerializer, RateCustomerSerializer, RentalDeleteSerializer, RentalSerializer, ProfileSerializer, FavoritesSerializer, RentalLikeSerializer, UserRentalListSerializer, DisplayRentalSerializer, UserFavoriteSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Rental, Profile, Favorites, RentalLike, ChatRoom, Message, RateOwner, RateCustomer, Comments
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework import status, viewsets
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView

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
        
        
class RemoveFavoriteView(generics.DestroyAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        # Get the favorite based on the user and post
        user = self.request.user
        post_id = self.kwargs['post_id']  # Assuming the post ID is passed in the URL
        return Favorites.objects.get(user=user, post_id=post_id)        
        
class UserFavoritesListAPIView(generics.ListAPIView):
    serializer_class = UserFavoriteSerializer

    def get_queryset(self):
        user = self.request.user
        return Favorites.objects.filter(user=user)
    
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
    
    
    
    
class RentalLikeCreateAPIView(generics.CreateAPIView):
    serializer_class = RentalLikeSerializer

    def create(self, request, *args, **kwargs):
        rental_id = kwargs.get('rental_id')
        print(f"Rental ID received: {rental_id}")
        print(f"User making request: {request.user}")

        try:
            rental = Rental.objects.get(id=rental_id)
        except Rental.DoesNotExist:
            print("Rental does not exist.")
            return Response({"detail": "Rental not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already liked this rental
        if RentalLike.objects.filter(user=request.user, rental=rental).exists():
            print(f"User {request.user} has already liked rental {rental_id}.")
            return Response({"detail": "You have already liked this rental."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a RentalLike instance
        rental_like = RentalLike(user=request.user, rental=rental)
        rental_like.save()
        serializer = self.get_serializer(rental_like)

        print(f"Like created for rental {rental_id} by user {request.user}.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    
class RentalLikeCountView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, rental_id):
        rental = Rental.objects.get(id=rental_id)
        like_count = rental.likes.count()  # Assuming 'likes' is a related field
        return Response({"likes_count": like_count})
    
    
class RentalLikeDeleteAPIView(APIView):
    def delete(self, request, rental_id):
        rental = Rental.objects.get(id=rental_id)
        user = request.user

        # Check if the user has liked this rental
        rental_like = RentalLike.objects.filter(user=user, rental=rental)

        if rental_like:
            rental_like.delete()  # Remove the like
            return Response({"detail": "Rental has been unliked."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You haven't liked this rental."}, status=status.HTTP_400_BAD_REQUEST)




class ToggleRentalLikeAPIView(APIView):
    """
    Toggle like/unlike for a rental.
    """
    def post(self, request, rental_id):
        user = request.user
        print(f"User making request: {user}")
        print(f"Rental ID: {rental_id}")

        # Fetch the rental object or return 404 if not found
        rental = get_object_or_404(Rental, id=rental_id)

        # Check if a RentalLike already exists for this user and rental
        rental_like, created = RentalLike.objects.get_or_create(user=user, rental=rental)

        if created:
            # If created is True, it means a new like was added
            print(f"New like created for rental {rental_id} by user {user}.")
            return Response({"detail": "Rental has been liked."}, status=status.HTTP_201_CREATED)
        else:
            # If created is False, it means the like already existed, so we remove it
            rental_like.delete()
            print(f"Like removed for rental {rental_id} by user {user}.")
            return Response({"detail": "Rental has been unliked."}, status=status.HTTP_200_OK)






@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_chat_room_and_send_message(request, receiver_id):
    sender = request.user
    content = request.data.get('content')

    # Check if content is provided
    if not content:
        return Response({'error': 'Message content is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return Response({'error': 'Receiver does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    existing_chat_rooms = ChatRoom.objects.filter(users=sender).filter(users=receiver)

    if existing_chat_rooms.exists():
        chat_room = existing_chat_rooms.first()
    else:
        chat_room = ChatRoom.objects.create()
        chat_room.users.add(sender, receiver)

    message_data = {
        'chat_room': chat_room.id,
        'sender': sender.id,
        'content': content
    }
    message_serializer = MessageSerializer(data=message_data)

    if message_serializer.is_valid():
        message_serializer.save()
        return Response({
            'chat_room': ChatRoomSerializer(chat_room).data,
            'message': message_serializer.data
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_rooms_for_logged_in_user(request):

    user = request.user

    chat_rooms = ChatRoom.objects.filter(users=user)
    
    data = []
    for room in chat_rooms:
        other_users = room.users.exclude(id=user.id)
        latest_message = Message.objects.filter(chat_room=room).order_by('-timestamp').first()
        latest_message_content = latest_message.content if latest_message else "No messages yet"
        latest_message_timestamp = latest_message.timestamp if latest_message else None
        
        room_data = {
            'id': room.id,
            'other_users': [{'id': other_user.id, 'first_name': other_user.first_name, 'username': other_user.username} for other_user in other_users],
            'latest_message': latest_message_content,
            'timestamp': latest_message_timestamp
        }
        data.append(room_data)

    return Response(data, status=status.HTTP_200_OK)



class ChatRoomView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        other_user_id = self.kwargs['other_user_id']
        current_user_id = self.kwargs['current_user_id']

        other_user = get_object_or_404(User, id=other_user_id)
        current_user = get_object_or_404(User, id=current_user_id)

        chat_rooms = ChatRoom.objects.filter(users__in=[current_user, other_user]).distinct()

        chat_rooms = [chat_room for chat_room in chat_rooms if 
                      chat_room.users.filter(id=current_user_id).exists() and
                      chat_room.users.filter(id=other_user_id).exists()]
        
        return chat_rooms

    def list(self, request, *args, **kwargs):
        chat_rooms = self.get_queryset()
        chat_room_data = []
        for chat_room in chat_rooms:
            chat_room_serializer = ChatRoomSerializer(chat_room)
            chat_room_id = chat_room_serializer.data['id']
            print(f"Chat Room ID: {chat_room_id}")
            
            # Get messages for the chat room
            messages = Message.objects.filter(chat_room=chat_room_id).order_by('timestamp')
            print(f"Messages: {messages}")
            
            message_serializer = MessageSerializer(messages, many=True)
            
            chat_room_data.append({
                'chat_room_id': chat_room_id,
                'messages': message_serializer.data
            })

        return Response(chat_room_data, status=status.HTTP_200_OK)


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]  # Use AllowAny if public access is needed
    
    

class RateOwnerView(APIView):
    """
    Allow users to rate an owner.
    """
    permission_classes = [AllowAny]

    def post(self, request, ownerId, ratedById, *args, **kwargs):
        # Log received data
        print(f"Received data: {request.data}")

        # Validate owner exists
        try:
            owner = User.objects.get(id=ownerId)
        except User.DoesNotExist:
            return Response({"error": "The owner does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Validate rater exists
        try:
            rater = User.objects.get(id=ratedById)
        except User.DoesNotExist:
            return Response({"error": "The rater does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Extract and validate points
        points = request.data.get("points")
        if points is None:
            return Response({"error": "Points are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has already rated this owner
        if RateOwner.objects.filter(owner=owner, rate_by=rater).exists():
            return Response({"error": "You have already rated this owner."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the rating
        serializer = RateOwnerSerializer(data={"owner": owner.id, "rate_by": rater.id, "points": points})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckRatingView(APIView):
    """
    Check if a user has already rated a specific owner.
    """
    permission_classes = [AllowAny]

    def get(self, request, ownerId, ratedById, *args, **kwargs):
        # Check if a rating exists between this owner and rater
        already_rated = RateOwner.objects.filter(owner_id=ownerId, rate_by_id=ratedById).exists()
        return Response({"alreadyRated": already_rated})
    



class OwnerRatingAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, owner_id):
        try:
            # Get all ratings for the owner
            ratings = RateOwner.objects.filter(owner_id=owner_id)
            
            if not ratings.exists():
                return Response({
                    "owner_id": owner_id,
                    "average_rating": None,
                    "total_ratings": 0,
                    "points": [],
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Calculate the average rating
            total_points = sum(rating.points for rating in ratings)
            total_ratings = ratings.count()
            average_rating = round(total_points / total_ratings, 2)  # Rounded to 2 decimals
            
            # Extract individual points
            points = list(ratings.values_list('points', flat=True))
            
            return Response({
                "owner_id": owner_id,
                "average_rating": average_rating,
                "total_ratings": total_ratings,
                "points": points,
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        





class RateCustomerView(APIView):
    """
    Allow users to rate an owner.
    """
    permission_classes = [AllowAny]

    def post(self, request, customerId, ratedById, *args, **kwargs):
        # Log received data
        print(f"Received data: {request.data}")

        # Validate owner exists
        try:
            customer = User.objects.get(id=customerId)
        except User.DoesNotExist:
            return Response({"error": "The owner does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Validate rater exists
        try:
            rater = User.objects.get(id=ratedById)
        except User.DoesNotExist:
            return Response({"error": "The rater does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Extract and validate points
        points = request.data.get("points")
        if points is None:
            return Response({"error": "Points are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has already rated this owner
        if RateCustomer.objects.filter(customer=customer, rate_by=rater).exists():
            return Response({"error": "You have already rated this owner."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the rating
        serializer = RateCustomerSerializer(data={"customer": customer.id, "rate_by": rater.id, "points": points})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class CheckCustomerRatingView(APIView):
    """
    Check if a user has already rated a specific owner.
    """
    permission_classes = [AllowAny]

    def get(self, request, customerId, ratedById, *args, **kwargs):
        # Check if a rating exists between this owner and rater
        already_rated = RateCustomer.objects.filter(customer_id=customerId, rate_by_id=ratedById).exists()
        return Response({"alreadyRated": already_rated})
    
    
    
class CustomerRatingAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, customer_id):
        try:
            # Get all ratings for the owner
            ratings = RateCustomer.objects.filter(customer_id=customer_id)
            
            if not ratings.exists():
                return Response({
                    "customer_id": customer_id,
                    "average_rating": None,
                    "total_ratings": 0,
                    "points": [],
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Calculate the average rating
            total_points = sum(rating.points for rating in ratings)
            total_ratings = ratings.count()
            average_rating = round(total_points / total_ratings, 2)  # Rounded to 2 decimals
            
            # Extract individual points
            points = list(ratings.values_list('points', flat=True))
            
            return Response({
                "customer_id": customer_id,
                "average_rating": average_rating,
                "total_ratings": total_ratings,
                "points": points,
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class PostCommentAPIView(APIView):
    def post(self, request, commentor_id, post_id):
        try:
            # Fetch related objects
            commentor = User.objects.get(id=commentor_id)
            post = Rental.objects.get(id=post_id)
        except User.DoesNotExist:
            return Response({"error": "Commentor not found."}, status=status.HTTP_404_NOT_FOUND)
        except Rental.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        # Print received data for debugging
        print("Received data:", request.data)

        # Exclude 'post' and 'commentor' from the request data
        data = request.data.copy()  # Make a copy to avoid modifying the original request.data
        data['post'] = post.id
        data['commentor'] = commentor.id  # Pass just the user ID

        # Create a new comment
        serializer = CommentsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # commentor and post are automatically set
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Print validation errors for debugging
        print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class CommentsListAPIView(APIView):
    def get(self, request, post_id):
        try:
            # Ensure the post exists
            post = Rental.objects.get(id=post_id)
        except Rental.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get all comments for the specified post
        comments = Comments.objects.filter(post=post).order_by('-date_commented')
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class RentalDetailView(RetrieveAPIView):
    queryset = Rental.objects.all()  # Or apply any specific filter if needed
    serializer_class = RentalSerializer
    lookup_field = 'id'  # This assumes the parameter in the URL will be 'id'
    
    def get(self, request, *args, **kwargs):
        rental = self.get_object()
        serializer = self.get_serializer(rental)
        return Response(serializer.data)
    
    



class UnreadMessagesGlobalCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            # Validate the provided user_id
            current_user = User.objects.get(id=user_id)

            # Get the chat rooms the current user is part of
            user_chat_rooms = ChatRoom.objects.filter(users=current_user)

            # Count unread messages in those chat rooms where the sender is not the current user
            unread_count = Message.objects.filter(
                chat_room__in=user_chat_rooms,
                is_read=False
            ).exclude(sender=current_user).count()

            return Response({'unread_count': unread_count})

        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)
        
class MarkMessagesAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chat_room_id, user_id):
        try:
            # Validate the user
            current_user = User.objects.get(id=user_id)

            # Get the chat room
            chat_room = ChatRoom.objects.get(id=chat_room_id)

            # Check if the user is part of the chat room
            if not chat_room.users.filter(id=current_user.id).exists():
                return Response({'error': 'This user is not a member of the chat room.'}, status=403)

            # Update messages in the chat room, excluding messages sent by the current user
            updated_count = chat_room.messages.filter(
                is_read=False
            ).exclude(sender=current_user).update(is_read=True)

            return Response({
                'message': 'Messages marked as read successfully.',
                'updated_count': updated_count
            })

        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)
        except ChatRoom.DoesNotExist:
            return Response({'error': 'Chat room not found.'}, status=404)