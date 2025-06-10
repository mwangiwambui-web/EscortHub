from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Only create a profile for non-admin users
    if created and not instance.is_superuser and not instance.is_staff:
        from .models import Profile
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)
