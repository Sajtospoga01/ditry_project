from operator import mod
from pyexpat import model
from statistics import mode
from tkinter import CASCADE
from turtle import pos
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.db.models.constraints import UniqueConstraint

# Create your models here.
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
    # folder #
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(UserProfile,on_delete=CASCADE,related_name='%(class)s_requests_created')
    title = models.CharField(max_length=128,default="")
    likes = models.IntegerField(default=0)
    picture = models.ImageField(null = False,upload_to='backend')
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
        return self.follower.username + ' follows: '+self.following.name
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
    category = models.ForeignKey(Post,on_delete=CASCADE,related_name='%(class)s_in_category')

    class Meta:
        constraints = [
            UniqueConstraint(fields = ['post','category'], name = 'Categorises')
        ]
    def __str__(self):
        return self.post.id + ' belongs to: ' +self.category.name


class Folder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id','name'], name = 'Folder')
        ]

class Queries:
    def get_posts_in_category(category):
        results = Category.objects.select_related().get(Category.name == category)
        return results

    def get_user_posts(user):
        result = UserProfile.objects.select_related().get(UserProfile.user.username == user)
        return result

    def get_user_follows(user):
        result = UserProfile.objects.select_related().get(UserProfile.user.username == user)
