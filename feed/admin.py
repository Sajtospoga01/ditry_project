from django.contrib import admin
from feed.models import Category,Post,UserProfile,Comment,FollowsCategory,Folder,In_folder

class PostAdmin(admin.ModelAdmin):
    list_display = ('creator', 'title', 'picture', 'likes')


class UserAdmin(admin.ModelAdmin):
    list_disply = ('username', 'email', 'posts', 'follows', 'followers')

    def posts(self,obj):
        return get_user_posts(obj.id).count()
    def follows(self,obj):
        return get_user_follows(obj.id).count()
    def followers(self,obj):
        return get_user_following(obj.id).count()

admin.site.register(Category)
admin.site.register(UserProfile, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(FollowsCategory)
admin.site.register(Folder)
admin.site.register(In_folder)
# Register your models here.

