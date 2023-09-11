from django.urls import path
from users import views
from django.contrib.auth.views import LoginView, LogoutView
from users.apps import UsersConfig
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = UsersConfig.name

urlpatterns = [
   path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('register/', views.RegisterView.as_view(), name='register'),
   path('profile/', views.ProfileView.as_view(), name='profile'),

   path('token/', TokenObtainPairView.as_view(), name='token'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]