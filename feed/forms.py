from pydoc import describe
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from feed.models import Post, Folder, Comment, UserProfile, Categorises, Category
from string import Template
from django.utils.safestring import mark_safe

class UserForm(UserCreationForm):
    ## this is for register
    email = forms.EmailField(required=True,help_text="Required, Add a valid email address")

    class Meta:
        model = UserProfile
        fields = {'username',
                  'first_name','last_name',
                  'email',
                  'password1',
                  'password2'}


class UserProfileForm(forms.Form):
    ## this is for editprofile
    class meta:
        model = UserProfile
        fields = {'website',
                  'bio',
                  'picture'}

class UserLoginForm(forms.ModelForm):
    ## this is for logins
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = {'username' , 'password'}

class PictureWidget(forms.widgets.Widget):

    def render(self, name, value, attrs=None, **kwargs):

        html =  Template("""<img src="$link"/>""")

        return mark_safe(html.substitute(link=value))

class UserPostsForm(forms.ModelForm):
    title = forms.CharField(max_length=24,required=True)
    picture = forms.ImageField(required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}), required=False)
    
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    original = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Post
        fields = {'title','picture'}

class PostCategoryForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Categorises
        fields = {'category',}

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=36)
    profile_picture = forms.ImageField()

    class Meta:
        model = User
        fields = {'username','profile_picture' }

class UserCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=128)

    class Meta:
        model = Comment
        fields = {'comment'}

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