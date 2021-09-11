
from django.urls import path
from .views import *

urlpatterns=[
    path('',login_view,name="login"),
    path('logout',login_view,name="logout"),
    path('register',register,name="register"),
    path('home/',home_view,name="home"),
    path('Profile/',my_profile_view,name="my-profile-view"),
    
    path('my-invite/',invites_received_view,name="my-invite"),
    path('all-profiles/',ProfileListView.as_view(),name="all-profiles-view"),
    path('to-invite/',invite_profiles_list_view,name='invite-profile'),
    path('send-invite/',send_invitation,name="send-invite"),
    path('remove-friend/',remove_from_friends,name="remove-friend"),
    path('my-invite/accept',accept_invitation,name="accept-invite"),
    path('my-invite/reject',reject_invitation,name="reject-invite"),
    path('Profile/<slug>/',ProfileDetailView.as_view(),name="profile-detail"),
    ]