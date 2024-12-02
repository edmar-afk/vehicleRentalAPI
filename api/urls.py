from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh_token'),
    
    path('createRental/', views.RentalSet.as_view(), name='create_rental'),
    path('rental/delete/<int:pk>/', views.RentalSet.as_view(), name='delete_rental'),
    
    path('user/', views.UserDetailView.as_view(), name='user_detail'),
    path('upload_picture/', views.ProfilePictureUpdateView.as_view(), name='upload_picture'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile_picture'),
    path('rentals/', views.RentalListAPIView.as_view(), name='rental-list'),
    
    path('favorites/', views.CreateFavoriteView.as_view(), name='create_favorite'),
    path('favorites/remove/<int:post_id>/', views.RemoveFavoriteView.as_view(), name='remove-favorite'),
    path('user/favorites/', views.UserFavoritesListAPIView.as_view(), name='user-favorites-list'),
    
    path('my-rentals/<int:user_id>/', views.UserRentalsView.as_view(), name='user-rentals'),
    path('rentals/<int:id>/delete/', views.RentalDeleteAPIView.as_view(), name='rental-delete'),
    path('rentals/<int:rental_id>/likes/', views.RentalLikeCreateAPIView.as_view(), name='rental-like-create'),
    path('rental/<int:rental_id>/likes/', views.RentalLikeCreateAPIView.as_view(), name='rental-like-create'),
    path('displayLikes/<int:rental_id>/', views.RentalLikeCountView.as_view(), name='display-likes'),
    path('rental/<int:rental_id>/unlike/', views.RentalLikeDeleteAPIView.as_view(), name='rental-like-delete'),
     path('rental/<int:rental_id>/toggle-like/', views.ToggleRentalLikeAPIView.as_view(), name='toggle-rental-like'),
    
    path('create-chat/<int:receiver_id>/', views.create_chat_room_and_send_message, name='create-chat'),
    path('my-chat-rooms/', views.get_chat_rooms_for_logged_in_user, name='my-chat-rooms'),
    path('chat_rooms/<int:other_user_id>/<int:current_user_id>/', views.ChatRoomView.as_view(), name='chat-room-list'),
    path('user/<int:id>/', views.UserDetailAPIView.as_view(), name='user-detail'),
    
    
    path('rate-owner/<int:ownerId>/<int:ratedById>/', views.RateOwnerView.as_view(), name='rate-owner'),
    path('check-rating/<int:ownerId>/<int:ratedById>/', views.CheckRatingView.as_view(), name='check-rating'),
    path('owner/<int:owner_id>/rating/', views.OwnerRatingAPIView.as_view(), name='owner-rating'),
    
    
    path('rate-customer/<int:customerId>/<int:ratedById>/', views.RateCustomerView.as_view(), name='rate-customer'),
    path('check-customer-rating/<int:customerId>/<int:ratedById>/', views.CheckCustomerRatingView.as_view(), name='check-customer-rating'),
    path('customer/<int:customer_id>/rating/', views.CustomerRatingAPIView.as_view(), name='customer-rating'),
    
    
    
    
    path('comments/<int:commentor_id>/<int:post_id>/', views.PostCommentAPIView.as_view(), name='post-comment'),
    path('comments/<int:post_id>/', views.CommentsListAPIView.as_view(), name='comments-list'),
    
    
    path('rental/<int:id>/', views.RentalDetailView.as_view(), name='rental-detail'),
    
    
    
    path('messages/unread-global/<int:user_id>/', views.UnreadMessagesGlobalCountView.as_view(), name='unread-messages-global-count'),
    path('chatrooms/<int:chat_room_id>/mark-read/<int:user_id>/', views.MarkMessagesAsReadView.as_view(), name='mark-messages-as-read'),
]