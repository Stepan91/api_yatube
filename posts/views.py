from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly)

  
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    #queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]


    def get_queryset(self):
        post_id=self.kwargs['post_id']
        return Comment.objects.filter(post__id=post_id)

    # как тут в таком случае коммент привязывается к посту,
    # если я удалил post.comment = serializer.validated_data?
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)