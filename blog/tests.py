from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Category, Post

class UserLoginTestCase(APITestCase):
    def setUp(self):
      
        Post.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
        
        self.credentials = {
            'username': 'testuser',
            'password': 'testpassword',
            'email':'demo_user@fakedomain.com',
            'first_name': 'User',
            'last_name': 'Demo'
        }
        self.user = User.objects.create_user(**self.credentials)
        self.token_url = reverse('login')

    def test_token_login(self):
        # Simulate login to get token
        response = self.client.post(self.token_url, self.credentials)
        print(response.data)
        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the token is in the response
        self.assertIn('token', response.data)

        # Use the token to authenticate further requests
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

class PostTestCase(APITestCase):
    def setUp(self):
        Post.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
        
        self.credentials = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'demo_user@fakedomain.com',
            'first_name': 'User',
            'last_name': 'Demo'
        }
        self.user = User.objects.create_user(**self.credentials)
        
        # Create category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            description='Test Category Description'
        )
        
        # Login to get token
        response = self.client.post(reverse('login'), self.credentials)
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        
        # URLs
        self.create_post_url = reverse('post-list')
        self.list_posts_url = reverse('post-list')

    def test_create_post(self):
        """Test creating a new post"""
        post_data = {
            'title': 'Test Post',
            'content': 'Test Content',
            'category': self.category.id,
            'status': 'published'
        }
        
        response = self.client.post(self.create_post_url, post_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Test Post')
        self.assertEqual(Post.objects.get().author, self.user)

    def test_list_posts(self):
        """Test listing posts"""
        # Create a test post first
        Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user,
            category=self.category,
            status='published',
            slug='test-post'
        )
        response = self.client.get(self.list_posts_url)
        
        self.user.is_staff = True
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Response data:", response.data)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Post')
        self.assertEqual(response.data[0]['author']['username'], 'testuser')
        
        # Verify like/dislike counts are present
        self.assertIn('like_count', response.data[0])
        self.assertIn('dislike_count', response.data[0])
        self.assertIn('user_has_liked', response.data[0])
        self.assertIn('user_has_disliked', response.data[0])
        
    def test_delete_own_post(self):
        """The user can delete his own post"""
        # Crear post como el usuario actual
        post = Post.objects.create(
            title='Post to delete',
            content='Content',
            author=self.user,
            category=self.category,
            status='published',
            slug='post-to-delete'
        )
        post.save()
        print(f"Slug real del post creado: {post.slug}")
        print("Post slug:", post.slug)
        print("DELETE URL:", reverse('post-detail', kwargs={'slug': post.slug}))
        print("Todos los posts:", Post.objects.all())
        
        delete_url = reverse('post-detail', kwargs={'slug': post.slug})
        response = self.client.delete(delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def test_user_cannot_delete_others_post(self):
        """A user can't delete the don't post owned by him"""
        other_user = User.objects.create_user(username='other', password='otherpass')
        post = Post.objects.create(
            title='Other user post',
            content='No borrar',
            author=other_user,
            category=self.category,
            status='published',
            slug='other-user-post'
        )
        post.save()
        print(f"Slug real del post creado: {post.slug}") 
        
        delete_url = reverse('post-detail', kwargs={'slug': post.slug})
        response = self.client.delete(delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())

    def test_view_post_detail(self):
        post = Post.objects.create(
            title='Post de prueba',
            content='Contenido completo del post',
            author=self.user,
            category=self.category,
            status='published',
            slug='post-de-prueba'
        )

        url = reverse('post-detail', kwargs={'slug': post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Post de prueba')
        self.assertEqual(response.data['author']['username'], self.user.username)
        
    def test_user_can_view_own_posts(self):
        # Create posts by the authenticated user
        Post.objects.create(
            title='My Post 1',
            content='Content',
            author=self.user,
            category=self.category,
            status='draft',
            slug='my-post-1'
        )
        Post.objects.create(
            title='My Post 2',
            content='Content',
            author=self.user,
            category=self.category,
            status='published',
            slug='my-post-2'
        )

        # Create a post by another user
        other = User.objects.create_user(username='other', password='123')
        Post.objects.create(
            title='Other user post',
            content='Should not be visible',
            author=other,
            category=self.category,
            status='published',
            slug='other-post'
        )

        url = reverse('post-my-posts')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for post in response.data:
            self.assertEqual(post['author']['username'], self.user.username)

