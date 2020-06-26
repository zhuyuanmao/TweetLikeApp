from django.urls import path
from django.conf.urls import include

from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter(trailing_slash=False)
router.register('posts',PostViewSet)

urlpatterns = [
    path('',include(router.urls)),
]