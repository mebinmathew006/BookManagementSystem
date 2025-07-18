from django.urls import path
from .views import UserSignupView,Login,Profile
from rest_framework_simplejwt.views import  TokenRefreshView



urlpatterns = [
    path('signup',UserSignupView.as_view() , name= 'signup'),
    path('login',Login.as_view() , name= 'login'),
    path('profile',Profile.as_view() , name= 'profile'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),  
]