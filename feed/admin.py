from django.contrib import admin
from feed.models import Category,Post,UserProfile,Comment,FollowsCategory,Folder,In_folder, Queries

class CommentInline(admin.TabularInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('creator', 'title', 'likes', 'comments')

    inlines = [CommentInline]

    def comments(self, obj):
        return len(Queries.get_comment_on_post(obj.id))

class PostInline(admin.TabularInline):
    model = Post

class FollowCategoryInline(admin.TabularInline):
    model = FollowsCategory

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'posts', 'follows', 'followers')

    inlines = [PostInline, FollowCategoryInline]

    def email(self, obj):
        return obj.email
    def posts(self,obj):
        p = Queries.get_user_posts(obj.id)
        if p != None: return len(p)
        return 0
    def follows(self,obj):
        f = Queries.get_user_follows(obj.id)
        if f != None: return len(f)
        return 0
    def followers(self,obj):
        f = Queries.get_user_following(obj.id)
        if f != None: return len(f)
        return 0

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'post', 'likes')

class InFolderInline(admin.TabularInline):
    model = In_folder

class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'posts', 'private')

    inlines = [InFolderInline]

    def posts(self, obj):
        p = Queries.get_posts_in_folder(obj.id)
        if p!= None: return len(p)
        return 0

admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Folder, FolderAdmin)
# Register your models here.
# follows category not included, can be done through each userprofile
# same with in_folder through folder admin
