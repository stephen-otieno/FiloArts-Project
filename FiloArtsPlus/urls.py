from FiloArts import settings
from . import views
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='homepage'),
    path('client_data/', views.client_data, name='client_data'),
    path('gallery/', views.gallery, name='gallery'),
    # path('blog_upload/',views.blog_detail, name='blog_detail'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),

    path('blogs/', views.blog_list, name='blogs'),
    path('login/', views.login_page, name='login'),
    path('drawing_upload/', views.drawing_upload, name='uploads'),

    path('stk_push/', views.stk_push, name='stk_push'),
    path('callback', views.callback, name='callback'),
    path('waiting/<int:transaction_id>/', views.waiting_page, name='waiting_page'),
    path('check_status/<int:transaction_id>/', views.check_status, name='check_status'),

    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('payment-cancelled/', views.payment_failed, name='payment_cancelled'),
    path('pay/', views.pay, name='pay'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



 # path('clients/', views.view_clients, name='clients'),
    # path('signup/',views.signup_page, name='signup'),

