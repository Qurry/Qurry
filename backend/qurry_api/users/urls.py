from django.urls import path

from .views import Accounting, ProfileView, UserView

urlpatterns = [

    path('login/', Accounting().login, name='login'),
    path('register/', Accounting().register, name='register'),
    path('activate/<str:uid>/<str:token>/',
         Accounting().activate, name='activate-account'),

    path('users/', UserView.as_view(), name='view-users'),
    path('users/<str:id>/', UserView.as_view(), name='view-user-details'),

    path('profile/', ProfileView.as_view(), name='view-profile'),
]
