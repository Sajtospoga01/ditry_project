from pydoc import describe
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from feed.models import Post, Folder, Comment, UserProfile, Categorises, Category, Queries, In_folder
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
    # deprecated, delete
    class meta:
        model = UserProfile
        fields = {'website',
                  'bio',
                  'profile_picture'}

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
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}), required=False)
    
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    original = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Post
        fields = {'title','picture','description'}

class PostCategoryForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Categorises
        fields = {'category',}

class EditProfileForm(forms.ModelForm):
    website = forms.URLField(help_text="Enter one of your socials here!")
    bio = forms.CharField(help_text="Describe youself... ",max_length=256)
    profile_picture = forms.ImageField(required=False)

    class meta:
        model = UserProfile
        fields = {'website',
                  'bio',
                  'profile_picture'}

class UserCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=128)

    class Meta:
        model = Comment
        fields = {'comment'}

class FolderForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = Folder
        fields = {'name'}
class AddPostToFolderForm(forms.ModelForm):
    folder_list = None
    folder = None
    post = None
    class Meta:
        model = In_folder
        fields = {'folder','post',}
    def __init__(self,cur_user,*args,**kwargs):
        ## this should technically pull the folders that the user has, but it returns the dummy folders 
        super(AddPostToFolderForm,self).__init__(*args,**kwargs)
        self.fields['folder_list'] = forms.ModelChoiceField(Queries.get_user_folders(cur_user.id))
class ResetForm(forms.ModelForm):
    email = forms.EmailField()
    new_password = forms.PasswordInput()

    class Meta:
        model = User
        fields = {'email','password'}