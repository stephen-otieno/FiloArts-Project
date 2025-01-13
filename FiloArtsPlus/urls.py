from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='homepage'),
    path('gallery/', views.gallery, name='gallery'),
    path('blogs/', views.blogs, name='blogs'),
]