from django.contrib import admin
from feed.models import Category,Post,UserProfile,Comment,FollowsCategory,Folder,In_folder

admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(FollowsCategory)
admin.site.register(Folder)
admin.site.register(In_folder)

# Register your models here.

