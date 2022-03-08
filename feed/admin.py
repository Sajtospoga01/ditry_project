from django.contrib import admin
from feed.models import UserProfile,Category,Post,Comment,Categorises,FollowsUser


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Categorises)
admin.site.register(FollowsUser)


# Register your models here.
