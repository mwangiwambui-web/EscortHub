from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class Profile(models.Model):
    CATEGORY_CHOICES = [
        ('VIP', 'VIP'),
        ('Regular', 'Regular'),
        ('Basic', 'Basic'),
    ]
        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    age = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    town = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='Regular')

    def __str__(self):
        return self.user.username

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    views = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title