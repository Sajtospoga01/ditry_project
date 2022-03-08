from cgitb import reset
from operator import mod
from pyexpat import model
from statistics import mode
from tkinter import CASCADE
from turtle import pos
from unicodedata import category
from unittest import result
from django.db import models
from django.contrib.auth.models import User
from django.db.models.constraints import UniqueConstraint

# Create your models here.

# 
#
#
#
#
#
#
#


class UserProfile(User):
    
    profile_picture = models.ImageField(blank = True)
    def __str__ (self):
        return self.username + ' '+ str(self.id)

    

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32,unique=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'
    

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(UserProfile,on_delete=CASCADE,related_name='%(class)s_requests_created')
    title = models.CharField(max_length=128,default="")
    likes = models.IntegerField(default=0)
    picture = models.ImageField(null = False,upload_to='backend')
    original = models.IntegerField(null = True)
    def __str__(self):
        return self.title

class Comment(models.Model):  
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='%(class)s_on_post')
    user_id = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='%(class)s_by_user')
    class Meta:
        constraints = [
            UniqueConstraint(fields = ['id', 'post_id','user_id'], name = 'Comment')
        ]
    comment = models.CharField(max_length=256,blank=False)
    likes = models.IntegerField(default=0)
    def __str__(self):
        return self.comment

class FollowsUser(models.Model):
    follower = models.ForeignKey(UserProfile,on_delete=CASCADE,related_name='%(class)s_by_user')
    following = models.ForeignKey(UserProfile,on_delete=CASCADE,related_name='%(class)s_to_follow')

    def __str__(self):
        return self.follower.username + ' follows: '+self.following.username
    class Meta:
        constraints = [
            UniqueConstraint(fields = ['follower','following'], name = 'Follow_user')
        ]

class FollowsCategory(models.Model):
    follower = models.ForeignKey(UserProfile,on_delete=CASCADE,related_name='%(class)s_by_user')
    following = models.ForeignKey(Category,on_delete=CASCADE,related_name='%(class)s_to_follow')
    class Meta:
        constraints = [
            UniqueConstraint(fields = ['follower','following'], name = 'Follows_category')
        ]
    def __str__(self):
        return self.follower.username + ' follows: '+self.following.username
    

class Likes(models.Model):
    liker = models.ForeignKey(UserProfile,on_delete=CASCADE,related_name='%(class)s_by_user')
    liked_post = models.ForeignKey(Post,on_delete=CASCADE,related_name='%(class)s_on_post')
    class Meta:
        constraints = [
            UniqueConstraint(fields = ['liker','liked_post'], name = 'Likes')
        ]
    def __str__(self):
        return self.liker.username + ' liked: '+self.liked_post.id
    
class Categorises(models.Model):
    post = models.ForeignKey(Post,on_delete=CASCADE,related_name='%(class)s_post')
    category = models.ForeignKey(Category,on_delete=CASCADE,related_name='%(class)s_in_category')

    class Meta:
        constraints = [
            UniqueConstraint(fields = ['post','category'], name = 'Categorises')
        ]
    def __str__(self):
        return str(self.post.id) + ' belongs to: ' +self.category.name

class Functions:
    def connect_post_to_category(post,category):
        return Categorises.objects.get_or_create(post = post,category = category)

    def connect_user_likes_post(user,post):
        return Likes.objects.get_or_create(liker = post,liked_post = post)

    def connect_user_follows_category(user,category):
        return FollowsCategory.objects.get_or_create(follower = user,following = category)

    def connect_user_follows_user(user,followed):
        return FollowsUser.objects.get_or_create(follower = user,following = followed)

    

class Queries:
    #TODO: 
    # get_post_likes
    # get_follows_category
    # get_category_followers
    # get_original
    # get_attempts


    
    #takes user id
    def get_liked_posts(user):
        user_object = UserProfile.objects.get(id = id)
        filtered_likes = Likes.objects.filter(liker = user_object).values("liked_post")
        results = Post.objects.filter(id__in = filtered_likes)
        #returns a query of posts
        return results


    # takes a category name
    def get_posts_in_category(category): 
        category_object = Category.objects.get(name = category)
        filtered_posts = Categorises.objects.filter(category = category_object).values("post")
        results = Post.objects.filter(id__in = filtered_posts)
        #returns a query of posts
        return results

    #takes a post id
    def get_category_of_post(post):
        post_object = Post.objects.get(id = post)
       
        filtered_posts = Categorises.objects.filter(post = post_object).values("category")
        results = Category.objects.filter(id__in = filtered_posts)
        #returns a query of categories
        return results

    # takes a user id
    def get_user_posts(user):
        user_object = UserProfile.objects.get(id = user)
        result = Post.objects.filter(creator = user_object)
        #returns a query of posts
        return result

    #takes a user id
    def get_user_following(user):
        user_object = User.objects.get(id = user)
        filtered_users = FollowsUser.objects.filter(follower = user_object).values("following")
    
        result = UserProfile.objects.filter(id__in = filtered_users)
        #returns a query of userprofiles
        return result

    
    #takes a user id
    def get_user_follows(user):
        user_object = User.objects.get(id = user)
        filtered_users = FollowsUser.objects.filter(following = user_object).values("follower")
    
        result = UserProfile.objects.filter(id__in = filtered_users)
        #returns a query of userprofiles
        return result
