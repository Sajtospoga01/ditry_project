from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from feed.models import Post, Folder, Comment, UserProfile

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True,help_text="Required, Add a valid email address")

    class Meta:
        model = User
        fields = {'username',
                  'first_name','last_name',
                  'email',
                  'password1',
                  'password2'}


class UserProfileForm(forms.Form):
    class meta:
        model = UserProfile
        fields = {'website',
                  'bio',
                  'picture'}

class UserLoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = {'username' , 'password'}

class UserPostsForm(forms.ModelForm):
    title = forms.CharField(max_length=24,required=True)
    image = forms.ImageField()

    class Meta:
        model = Post
        fields = {'title','image'}

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
        model = Comment
        fields = {'user', 'content'}

class FolderForm(forms.ModelForm):
    foldername = forms.CharField()

    class Meta:
        model = Folder
        fields = {'name'}

class ResetForm(forms.ModelForm):
    email = forms.EmailField()
    new_password = forms.PasswordInput()

    class Meta:
        model = User
        fields = {'email','password'}