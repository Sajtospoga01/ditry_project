from django.contrib import admin
from feed.models import UserProfile,Category,Post,Comment


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(UserProfile)


# Register your models here.
