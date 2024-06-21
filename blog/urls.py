from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='post_edit'),
    path('reply_to_comment/<int:pk>/',views.reply_to_comment, name='reply_to_comment'),
    path('delete_comment/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('delete_reply/<int:pk>/', views.delete_reply, name='delete_reply'),
    path('markdownx/', include('markdownx.urls')),
    path('accounts/', include('allauth.urls')),
]
