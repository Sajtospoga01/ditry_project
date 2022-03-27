from django.urls import path
from feed import views

app_name ='feed'

urlpatterns = [
    path('', views.home, name ='home'),
    path('about/', views.about, name = 'about'),
    path('trending/', views.trending, name='trending'),
    path('help/', views.help, name='help'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('following/',views.userFollowing,name='following'),
    path('followers/',views.userFollowers,name='follower'),
    path('get-likes/',views.get_home_likes,name = 'get_likes'),
    path('get_follows/',views.get_follows,name = "get_follows"),

    path('show-category/<str:name_category>/', views.show_category, name='show_category'),
    
    path('show-post/<int:post_id>/', views.show_post, name='show_post'),
    path('show-post/<int:post_id>/like-post/', views.like_post, name='like_post'),
    path('show-post/<int:post_id>/save-post/', views.save_post, name='save_post'),
    path('show-post/<int:post_id>/add-to-folder/', views.add_post_to_folder, name='add_to_folder'),
    path('show-post/<int:post_id>/comment-on-post/', views.comment_on_post, name='comment_on_post'),
    path('show-post/<int:post_id>/<int:comment_id>/like-comment/', views.like_comment, name='like_comment'),

    path('add-post/', views.add_post, name='add_post'),
    path('add-post/<int:original_id>/', views.add_post, name='add_post'),
    path('account/<str:username>/', views.show_user, name='account'),
    path('<str:username>/folders/add-folder/', views.add_folder, name='add_folder'),

    path('<str:username>/folders/<int:folder_id>/', views.show_folder, name='show_folder'),
    path('<str:username>/my-attempts/', views.show_my_attempts, name='show_my_attempts'),
    path('<str:username>/update-profile/', views.update_profile,name='update_profile'),

    path('follow-user/<str:username>/', views.follow_user, name='follow_user'),
    path('follow-category/<slug:category_slug>/', views.follow_category, name='follow_category'),
    
    path('search-title/', views.search_title, name='search_title'),

]