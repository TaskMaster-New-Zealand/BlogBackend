from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication

from django.utils import timezone

from blog.permissions import IsAuthenticatedForLikeDislike
from .models import Category, Post, Comment
from .serializers import (CategorySerializer, PostListSerializer, 
                         PostDetailSerializer, PostCreateUpdateSerializer, CommentSerializer, UserSerializer)
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Try to authenticate the user
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid credentials. Please try again.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # If valid, proceed with token generation
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=200)

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Los permisos de lectura se permiten para cualquier solicitud
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Los permisos de escritura solo se permiten al autor del post
        return obj.author == request.user

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthorOrReadOnly | IsAuthenticatedForLikeDislike]
    authentication_classes = [TokenAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = Post.objects.all()
        
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostListSerializer
    
    @action(detail=True, methods=['post'])
    def publish(self, request, slug=None):
        post = self.get_object()
        if post.status == 'draft':
            post.status = 'published'
            post.published_at = timezone.now()
            post.save()
            serializer = self.get_serializer(post)
            return Response(serializer.data)
        return Response(
            {'status': 'failed', 'message': 'This post is already published'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, slug=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def toggle_dislike(self, request, slug=None):
        post = self.get_object()
        user = request.user
        
        # Remove like if it exists
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
        
        # Toggle dislike
        if post.dislikes.filter(id=user.id).exists():
            post.dislikes.remove(user)
            message = 'Dislike removed'
        else:
            post.dislikes.add(user)
            message = 'Dislike added'
        
        return Response({
            'status': 'success',
            'message': message,
            'like_count': post.likes.count(),
            'dislike_count': post.dislikes.count()
        })

    @action(detail=True, methods=['post'])
    def toggle_like(self, request, slug=None):
        post = self.get_object()
        user = request.user
        
        # Remove dislike if it exists
        if post.dislikes.filter(id=user.id).exists():
            post.dislikes.remove(user)
        
        # Toggle like
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            message = 'Like removed'
        else:
            post.likes.add(user)
            message = 'Like added'
        
        return Response({
            'status': 'success',
            'message': message,
            'like_count': post.likes.count(),
            'dislike_count': post.dislikes.count()
        })
