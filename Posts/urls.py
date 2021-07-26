#Posts
from django.urls import path
from .views import *

urlpatterns=[
    path('',post_comment_create_and_list_view,name="main-post-view"),
    path('Liked/',like_unlike_post,name="like-post-view"),
    path('<pk>/delete',PostDeleteView.as_view(),name="delete-post"),
    path('<pk>/update',PostUpdateView.as_view(),name="update-post")
    ]