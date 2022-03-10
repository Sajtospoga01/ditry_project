from django.contrib import admin
from feed.models import Category,Post,UserProfile,Comment,FollowsCategory

admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(FollowsCategory)
# Register your models here.

