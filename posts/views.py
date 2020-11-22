from rest_framework import viewsets
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status


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


    def get_queryset(self, *args, **kwargs):
        post_id=self.kwargs['post_id']
        post = Post.objects.get(id=post_id)
        if post:
            return post.comments
        return Response(status=status.HTTP_404_NOT_FOUND)

    # а зачем здесь проверка на наличие поста,
    # ведь мы это сделали при определении queryset,
    # который распространяется на все методы класса?
    def perform_create(self, serializer):
        post_id=self.kwargs['post_id']
        post = Post.objects.get(id=post_id)
        if post:
            serializer.save(author=self.request.user)
        return Response(status=status.HTTP_404_NOT_FOUND)