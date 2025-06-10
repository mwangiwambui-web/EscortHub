from django import forms
from django.contrib.auth.models import User
from .models import Profile, Video

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture', 'age', 'city', 'town', 'phone_number']

        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)        

    from .models import Video
    from django import forms
    
class VideoForm(forms.ModelForm):
        class Meta:
            model = Video
            fields = ['title', 'video_file']    