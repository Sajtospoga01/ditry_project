import imp
import os
from unicodedata import category

from django.forms import ImageField
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ditry_project.settings')
from PIL import Image
import django
django.setup()
from feed.models import Queries, User

def test_category_in_post():
    print("\nPost in category test...\n\n")
    categories = ["Cook","Diy","Craft"]
    for category in categories:
        print(category+" has posts:")
        posts = Queries.get_posts_in_category(category)
        print(posts)

def test_user_posts():
    print("\nUser posts test...\n\n")
    users = User.objects.all()
    for user in users:
        print(user.username+" created posts")
        posts = Queries.get_user_posts(user.id)
        for post in posts:
            print(post)

def test_following_user():
    print("\nUser following test...\n\n")

    users = User.objects.all()
    for user in users:
        print(str(user)+" follows:")
        follows = Queries.get_user_following(user.id)

        for following in follows:
            
            print(following)

def test_user_follows():
    print("\nUser follows test...\n\n")
    users = User.objects.all()
    for user in users:
        print(str(user)+" followed by:")
        follows = Queries.get_user_follows(user.id)

        for following in follows:
            
            print(following)

def test_get_category_of_post():
        print("\nUser follows test...\n\n")
     
        categories = Queries.get_category_of_post(1)
        for category in categories:
            print(category)

if __name__ == '__main__':
    test_category_in_post()
    test_user_posts()
    test_following_user()
    test_user_follows()
    test_get_category_of_post()