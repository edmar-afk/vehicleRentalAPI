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
    path('user/favorites/', views.UserFavoritesListAPIView.as_view(), name='user-favorites-list'),
    
    path('receiver/<int:userid>/', views.ReceiverDetailAPIView.as_view(), name='receiver-detail'),
    
]