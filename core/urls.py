from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'core'

urlpatterns = [
     path('', views.index, name='index'),
     path('videos/', views.video_list, name='video_list'),
     path('videos/<int:pk>/', views.video_detail, name='video_detail'),
     path('signup/', views.signup, name='signup'),
     path('login/', views.custom_login, name='login'),
     path('logout/', auth_views.LogoutView.as_view(next_page='core:login'), name='logout'),
     path('dashboard/', views.dashboard, name='dashboard'),
     path('my-videos/', views.user_videos, name='user_videos'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)