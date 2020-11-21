from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from rest_framework.authtoken import views

v1_router = DefaultRouter()
v1_router.register('posts', PostViewSet, basename = 'post-list')
v1_router.register('posts/(?P<post_id>.+)/comments', CommentViewSet, basename = 'comment-list')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]