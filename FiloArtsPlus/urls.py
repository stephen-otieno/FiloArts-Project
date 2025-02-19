from FiloArts import settings
from . import views
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='homepage'),
    path('client_data/', views.client_data, name='client_data'),
    path('gallery/', views.gallery, name='gallery'),
    path('blogs/', views.blogs, name='blogs'),
    path('clients/', views.view_clients, name='clients'),
    path('signup/',views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('drawing_upload/', views.drawing_upload, name='uploads'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)