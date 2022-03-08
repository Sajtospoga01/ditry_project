import os
from unicodedata import category

from django.forms import ImageField
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ditry_project.settings')
from PIL import Image
import django
django.setup()
from feed.models import Category,Post,UserProfile
from django.contrib.auth.models import User
from PIL import ImageFile

from django.core.files.images import ImageFile
from django.core.files import File

def populate():
    categories_populate = [
        {"name":"craft"},
        {"name":"Diy"},
        {"name":"Cook"}]
    post_populate = [
        {"id":1,
         "title":"title1",
         "likes":0,
         "picture": "sample_1.jpg",
         "creator":1
        },
        {"id":2,
         "title":"title2",
         "likes":0,
         "picture": "sample_2.jpg",
         "creator":1
        },
        {"id":3,
         "title":"title3",
         "likes":0,
         "picture": "sample_3.jpg",
         "creator":1
        }        
    ]
    test_profile = [
        {"username":"bob",
         "email":"example@example.com",
         "first_name":"bob",
         "last_name":"the builder",
         "password":"password"
        }
    ]
    for profile in test_profile:
  
        p = add_profile(profile["username"],profile["email"],profile["first_name"],profile["last_name"],profile["password"])
        print("user id:" +str(p.id))
        id = get_user(p.id)
        for post in post_populate:
            
            p = add_post(post["id"],post["title"],post["likes"],post["picture"],id)
           

    for cat in categories_populate:
        print(cat)
        add_category(cat["name"])
    
    for c in Category.objects.all():
        print(c.name)
        
    
def add_category(name):
    c = Category.objects.get_or_create(name = name)[0]
    c.save()
    return c

def add_post(id,title,likes,picture,creator):
    def_post = Post.objects.filter(id = id)
    if(def_post.count()==0):
        im = ImageFile(Image.open("sample_images/"+picture))
        c = Post.objects.create(id = id,creator = creator,title = title,likes = likes)
        c.picture.save(picture, ImageFile(open("sample_images/"+picture,"rb")))
    else:
        c = def_post[0]
    return c

def add_profile(username,email,first_name,last_name,password):
    def_user = UserProfile.objects.filter(username = username)
  
    if(def_user.count()==0):
        print("new user")
        user = UserProfile.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
      
        return user
    else:
        print("existing user")
        return def_user[0]   

    
def get_user(id):

    user = UserProfile.objects.get(id = id)
  
    return user
    


if __name__ == '__main__':
    print('Starting feed population script')
    populate()

    
    
