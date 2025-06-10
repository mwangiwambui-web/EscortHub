from django.shortcuts import render,redirect
from .models import Profile, Video
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from.forms import UserRegistrationForm, ProfileForm , LoginForm, VideoForm
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data.get('email')

            # Check for existing username or email
            if User.objects.filter(username=username).exists():
                user_form.add_error('username', 'A user with that username already exists.')
            elif email and User.objects.filter(email=email).exists():
                user_form.add_error('email', 'A user with that email already exists.')
            else:
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data['password'])
                    user.save()

                    # ✅ Get the auto-created profile and update extra fields
                    profile = Profile.objects.get(user=user)
                    profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
                    if profile_form.is_valid():
                        profile_form.save()

                return redirect('core:login')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    
    return render(request, 'core/signup.html', {'user_form': user_form, 'profile_form': profile_form})

def custom_login(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:dashboard')
            else:
                error = 'Invalid username or password.'
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form, 'error': error})

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

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('core:dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/dashboard.html', {'form': form, 'profile': profile})

@login_required
def user_videos(request):
    profile = request.user.profile
    videos = Video.objects.filter(profile=profile)
    if request.method == 'POST':
        video_form = VideoForm(request.POST, request.FILES)
        if video_form.is_valid():
            video = video_form.save(commit=False)
            video.profile = profile
            video.save()
            return redirect('core:user_videos')
    else:
        video_form = VideoForm()
    return render(request, 'core/user_videos.html', {
        'video_form': video_form,
        'videos': videos,
    })