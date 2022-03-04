from django import forms
from django.contrib.auth.models import User
from feed.models import post ## post changes to something else once models.py has been created

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=36)
    password = forms.CharField(widget=forms.PasswordInput())
    profile_picture = forms.ImageField()
    bio = forms.CharField(max_length=256)
    class Meta:
        model = User
        fields = ('username','password','email','profile_picture')
    
class UserLoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username' , 'password')

class UserPostsForm(forms.ModelForm):
    title = forms.CharField(max_length=24,required=True)
    image = forms.ImageField()
    likes = forms.IntegerField(default=0)
    comments = forms.CharField(max_length=248)

    class Meta:
        model = post
        fields = ('title','image','likes','comments')

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=36)
    profile_picture = forms.ImageField()

    class Meta:
        model = User
        fields = {'username','profile_picture' }

class UserCommentForm(forms.ModelForm):
    username = forms.CharField()
    content = forms.CharField(max_length=128)

    class Meta:
        model = User
        fields = {'user', 'content'}
