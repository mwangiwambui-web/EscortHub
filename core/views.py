from django.shortcuts import render
from .models import Profile, Video
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

def index(request):
    query = request.GET.get('q')
    cities = Profile.objects.values_list('city', flat=True).distinct()

    if query:
        filter_condition = Q(city__icontains=query) | Q(town__icontains=query)
        vip_profiles = Profile.objects.filter(filter_condition, category='VIP')
        regular_profiles = Profile.objects.filter(filter_condition, category='Regular')
        basic_profiles = Profile.objects.filter(filter_condition, category='Basic')
    else:
        vip_profiles = Profile.objects.filter(category='VIP')
        regular_profiles = Profile.objects.filter(category='Regular')
        basic_profiles = Profile.objects.filter(category='Basic')

    context = {
        'vip_profiles': vip_profiles,
        'regular_profiles': regular_profiles,
        'basic_profiles': basic_profiles,
        'cities': cities,
        'active_city': query or '',
    }
    return render(request, 'core/index.html', context)

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'core/video_list.html', {'videos': videos})

def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.views += 1
    video.save()
    return render(request, 'core/video_detail.html', {'video': video})