from django.contrib import admin
from .models import Profile
from .models import Video

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'age', 'city', 'town', 'phone_number')
    search_fields = ('user__username', 'city', 'town', 'phone_number')
    list_filter = ('city', 'town')

admin.site.register(Video)