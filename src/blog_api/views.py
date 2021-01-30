from django.shortcuts import get_object_or_404
from blogapp.models import Post, Like, PostView
from rest_framework.response import Response
from .serializers import PostCreateUpdateSerializer, PostListSerializer, PostDetailSerializer, CommentCreateSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwner
from .pagination import PostPageNumberPagination
from blog_api import serializers



class PostList(generics.ListAPIView):

    permission_classes = [AllowAny]
    pagination_class = PostPageNumberPagination
    serializer_class = PostListSerializer
    queryset = Post.objects.filter(status="p")


class UserPostList(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = PostPageNumberPagination
   
    # queryset = Post.objects.filter(author=request.user)

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user)
        return queryset




class PostCreateApi(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)




class PostDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = "slug"

    def get_object(self):
        obj = super().get_object()
        PostView.objects.get_or_create(user=self.request.user, post=obj)
        return obj



class PostUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = "slug"

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDelete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = "slug"


class CreateCommentAPI(APIView):
    """
    post:
        Create a comment instance. Returns created comment data
        parameters: [slug, body]
    """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = CommentCreateSerializer

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)



class CreateLikeAPI(APIView):

    permission_classes = [IsAuthenticated]
    # serializer_class = CommentCreateSerializer

    def post(self, request, slug):
        obj = get_object_or_404(Post, slug=slug)
        like_qs = Like.objects.filter(user=request.user, post=obj)
        if like_qs.exists():
            like_qs[0].delete()
        else:
            Like.objects.create(user=request.user, post=obj)

        data = {
            "messages": "like"
        }
        return Response(data)

