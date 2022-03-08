from django import forms
from django.contrib.auth.models import User
from feed.models import Post,Comment,UserProfile

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=36)
    # bio = forms.CharField(max_length=256) maybe at some point
    
    class Meta:
        model = User
        fields = ('username','password')

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    profile_picture = forms.ImageField()

    class Meta:
        model = User
        fields = {'password','profile_picture'}
class UserLoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username' , 'password')

class UserPostsForm(forms.ModelForm):
    title = forms.CharField(max_length=24,required=True)
    image = forms.ImageField()

    class Meta:
        model = Post
        fields = ('title','likes','picture')

class EditProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField()

    class Meta:
        model = UserProfile
        fields = {'profile_picture'}

class UserCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=128)

    class Meta:
        model = Comment
        fields = {'comment'}
