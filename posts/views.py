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

    
    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]


    def list(self, request, id=None):
        queryset = Comment.objects.filter(post__id=id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, id=None):
        post = get_object_or_404(Post, author=request.user, id=id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            post.comment = serializer.validated_data
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)