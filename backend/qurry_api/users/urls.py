from django.urls import path

from .views import Accounting, ProfileView, UserView

urlpatterns = [

    path('login/', Accounting().login, name='login'),
    path('register/', Accounting().register, name='register'),
    path('activate/<str:uid>/<str:token>/',
         Accounting().activate, name='activate-account'),
    path('forgotpassword/', Accounting().forgot_password, name='forgot-password'),
    path('resetpassword/<str:uid>/<str:token>/',
         Accounting().reset_password, name='reset-password'),
    path('resetpassword/', Accounting().set_password, name='set-password'),

    path('users/', UserView.as_view(), name='view-users'),
    path('users/<str:id>/', UserView.as_view(), name='view-user-details'),

    path('profile/', ProfileView.as_view(), name='view-profile'),

]
