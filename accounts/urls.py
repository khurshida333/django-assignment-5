from django.urls import path,include
from .views import UserRegistrationView, UserLoginView , UserLogoutView ,UserBankAccountUpdateView,ProfilePageView

app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register' ),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('update-profile/', UserBankAccountUpdateView.as_view(), name='update_profile' ),
    path('profile/', ProfilePageView.as_view(), name='profile'),
    
]
