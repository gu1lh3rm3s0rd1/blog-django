from django.urls import path
from . import views

urlpatterns = [
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
]
