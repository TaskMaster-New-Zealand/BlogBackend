from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'posts', views.PostViewSet)

urlpatterns = router.urls
urlpatterns.append(path('register/', views.RegisterView.as_view(), name='register'))