from rest_framework import serializers
from .models import Category, Post, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password' , 'email', 'first_name', 'last_name']
        
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at']
        read_only_fields = ['slug']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'email', 'content', 'created_at', 'approved']
        read_only_fields = ['approved']

class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    user_has_disliked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug','content', 'author', 'category', 'status', 
                 'created_at', 'updated_at', 'published_at', 'comment_count',
                 'like_count', 'dislike_count', 'user_has_liked', 'user_has_disliked']
        read_only_fields = ['slug']
    
    def get_comment_count(self, obj):
        return obj.comments.filter(approved=True).count()

    def get_like_count(self, obj):
        return obj.likes.count()
    
    def get_dislike_count(self, obj):
        return obj.dislikes.count()

    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def get_user_has_disliked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.dislikes.filter(id=request.user.id).exists()
        return False

class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    user_has_disliked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'author', 'category', 
                  'status', 'created_at', 'updated_at', 'published_at', 
                  'comments', 'like_count', 'dislike_count',
                  'user_has_liked', 'user_has_disliked']
        read_only_fields = ['slug']
    
    def get_comments(self, obj):
        comments = obj.comments.filter(approved=True)
        return CommentSerializer(comments, many=True).data

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False        


    def get_dislike_count(self, obj):
        return obj.dislikes.count()

    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def get_user_has_disliked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.dislikes.filter(id=request.user.id).exists()
        return False

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'status', 'published_at']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)