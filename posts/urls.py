from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from rest_framework.authtoken import views

v1_router = DefaultRouter()
v1_router.register('api/v1/posts', PostViewSet, basename = 'post-list')
v1_router.register('api/v1/posts/(?P<id>.+)/comments', CommentViewSet, basename = 'comment-list')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
]