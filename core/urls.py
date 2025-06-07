from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
     path('', views.index, name='index'),
     path('videos/', views.video_list, name='video_list'),
     path('videos/<int:pk>/', views.video_detail, name='video_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)