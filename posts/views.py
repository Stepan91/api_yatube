from rest_framework import viewsets
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer, CommentSerializer
from django.http import Http404


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
        try:
            post_id=self.kwargs['post_id']
            post = Post.objects.filter(id=post_id)
            return post[0].comments
        except Post.DoesNotExist:
            raise Http404

    def perform_create(self, serializer):
        try:
            post_id=self.kwargs['post_id']
            post_exists = Post.objects.filter(id=post_id).exists()
            serializer.save(author=self.request.user)
        except Post.DoesNotExist:
            raise Http404