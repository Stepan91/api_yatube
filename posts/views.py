from rest_framework import viewsets
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly)

  
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly)


    def get_queryset(self):
        post_id=self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        if post:
            return post.comments

    def perform_create(self, serializer):
        post_id=self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        if post:
            serializer.save(author=self.request.user)