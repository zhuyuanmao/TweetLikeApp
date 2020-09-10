from django.urls import path
from django.conf.urls import include

from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    CommentsListCreateAPIView,
    CommentDestroyAPIView,
    PostFavoriteAPIView
)

router = DefaultRouter(trailing_slash=False)
router.register('posts',PostViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('posts/<str:post_slug>/comments/',CommentsListCreateAPIView.as_view()),
    path('posts/<str:post_slug>/comments/<str:comment_pk>/',CommentDestroyAPIView.as_view()),
    path('post/<str:post_slug>/favorite/',PostFavoriteAPIView.as_view())
]