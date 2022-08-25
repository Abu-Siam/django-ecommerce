from django.urls import path
from account.views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,\
    UserPasswordResetEnterPhoneView,EditUserProfileView

urlpatterns =[
    path('signup/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/<uid>/<token>/', UserChangePasswordView.as_view(), name='change-password'),
    path('forgot-password-enter-phone/', UserPasswordResetEnterPhoneView.as_view(), name='change-password-enter-phone'),
    path('edit-profile/', EditUserProfileView.as_view(), name='edit-profile'),

]