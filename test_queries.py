import imp
import os
from turtle import pos
from unicodedata import category

from django.forms import ImageField
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ditry_project.settings')
from PIL import Image
import django
django.setup()
from feed.models import Category, Folder, Queries, User,Post, UserProfile

def test_category_in_post():
    print("\nPost in category test...\n")
    categories = Category.objects.all()
    for category in categories:
        print(str(category)+" has posts:")
        posts = Queries.get_posts_in_category(category.name)
        print(posts)

def test_user_posts():
    print("\nUser posts test...\n")
    users = UserProfile.objects.all()
    for user in users:
        print(user.username+" created posts")
        posts = Queries.get_user_posts(user.id)
        if posts != None:
            for post in posts:
                print(post)

def test_following_user():
    print("\nUser following test...\n")

    users = UserProfile.objects.all()
    for user in users:
        print(str(user)+" follows:")
        follows = Queries.get_user_following(user.id)

        for following in follows:
            
            print(following)

def test_user_follows():
    print("\nUser follows test...\n")
    users = UserProfile.objects.all()
    for user in users:
        print(str(user)+" followed by:")
        follows = Queries.get_user_follows(user.id)

        for following in follows:
            
            print("\t"+str(following))

def test_get_category_of_post():
    print("\ntest_get_category_of_post...\n")
    posts = Post.objects.all()
    for post in posts:
        print(str(post)+":")
    
        categories = Queries.get_category_of_post(post.id)
        for category in categories:
            print("\t"+str(category))

def test_get_post_likes():
    print("\ntest_get_post_likes...\n")
    posts = Post.objects.all()
    for post in posts:
        num = Queries.get_post_likes(post.id).count()
        print(str(post.id)+": "+str(num))

def test_get_liked_posts():
    print("\ntest_get_liked_posts...\n")
    users = UserProfile.objects.all()
    for user in users:
        print(user.username+" liked:")
        posts = Queries.get_liked_posts(user.id)
        for post in posts:
            print("\t"+post.title + " "+str(post.id))

def test_post_liked_by():
    print("\ntest_post_liked_by...\n")
    posts = Post.objects.all()
    for post in posts:
        print(str(post.id)+" liked by:")
        likes = Queries.get_post_likes(post.id)
        for like in likes:
            print("\t"+str(like.username))

def test_get_attempts():
    print("\ntest_get_attempts...\n")
    original_post = Post.objects.get(id = 1)
    print("Attempts for "+str(original_post)+":")
    attempts = Queries.get_attempts(original_post.id)
    for attempt in attempts:
        print(attempt)

def test_get_original():
    print("\ntest_get_original...\n")
    posts = Post.objects.all()
    for post in posts:
        original_post = Queries.get_original(post.id)
        print("Original post of "+str(post.id)+":")
        print(original_post)


def test_get_category_follows():
    print("\ntest_get_category_follows...\n")
    categories = Category.objects.all()
    for category in categories:
        followers = Queries.get_category_follows(category.name)
        print(str(category)+": ")
        for follower in followers:
            print("\t"+str(follower))

def test_get_category_following():
    print("\ntest_get_category_following...\n")
    users = UserProfile.objects.all()
    for user in users:
        print(str(user)+":")
        categories = Queries.get_category_following(user.id)
        for category in categories:
            print("\t"+category.name)

def test_get_comment():
    print("\ntest_get_comment...\n")
    posts = Post.objects.all()
    for post in posts:
        print(str(post)+" has comment:")
        comments = Queries.get_comment_on_post(post.id)
        for comment in comments:
            print("\t"+str(comment))
            print("\tposted by "+str(comment.user))

def test_get_posts_in_folder():
    print("\ntest_get_posts_in_folder...\n")
    folders = Folder.objects.all()
    for folder in folders:
        print(folder)
        posts = Queries.get_posts_in_folder(folder.id)
        for post in posts:
            print(post)

def test_get_user_folders():
    print("\ntest_get_user_folders...\n")
    users = UserProfile.objects.all()
    for user in users:
        print(user)
        folders = Queries.get_user_folders(user.id)
        for folder in folders:
            print("\t"+str(folder))

def test_get_user_attempts():
    print("\ntest_get_user_attempts...\n")
    users = UserProfile.objects.all()
    for user in users:
        print(user)
        attempts = Queries.get_user_attempts(user.id)
        if attempts != None:
            for attempt in attempts:
                print("\t"+ str(attempt))
        






if __name__ == '__main__':
    test_category_in_post()
    test_user_posts()
    test_following_user()
    test_user_follows()
    test_get_category_of_post()
    test_get_post_likes()
    test_get_liked_posts()
    test_post_liked_by() 
    test_get_attempts()
    test_get_original()
    test_get_category_follows()
    test_get_category_following()
    test_get_comment()
    test_get_posts_in_folder()
    test_get_user_folders()
    test_get_user_attempts()

