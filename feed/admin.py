from django.contrib import admin
from feed.models import Category,Post,UserProfile,Comment

admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
# Register your models here.

