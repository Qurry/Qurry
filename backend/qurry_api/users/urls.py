from django.urls import path

from .views import AccountingView, ProfileView, UserView

urlpatterns = [

    path('login/', AccountingView().login, name='login'),
    path('register/', AccountingView().register, name='register'),
    path('activate/<str:uid>/<str:token>/',
         AccountingView().activate, name='activate-account'),
    path('forgotpassword/', AccountingView().forgot_password, name='forgot-password'),
    path('resetpassword/<str:uid>/<str:token>/',
         AccountingView().reset_password, name='reset-password'),
    path('resetpassword/', AccountingView().set_password, name='set-password'),

    path('users/', UserView.as_view(), name='view-users'),
    path('users/<str:id>/', UserView.as_view(), name='view-user-details'),

    path('profile/', ProfileView.as_view(), name='view-profile'),

]
