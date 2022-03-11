from django.urls import path
from feed import views

app_name ='feed'

urlpatterns = [
    path('', views.home, name ='home'),
    path('about/', views.about, name = 'about'),
    path('add-post/', views.add_post, name='add_post'),
    path('trending/', views.trending, name='trending'),
    path('help/', views.help, name='help'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('add-post-to-category/', view.add_post_to_category, name='add_post_to_category'),
    path('food/', views.show_food, name='show_food'),
    path('diys/', views.show_diys, name='show_diys'),
    path('drafts/', views.show_drafts, name='show_drafts'),
    
    path('show-post/<int:post_id>/', views.show_post, name='show_post'),
    path('show-post/<int:post_id>/like-post/', views.like_post, name='like_post'),
    path('show-post/<int:post_id>/save-post/', views.save_post, name='save_post'),
    path('show-post/<int:post_id>/comment-on-post/', views.comment_on_post, name='comment_on_post'),
    path('show-post/<int:post_id>/<int:comment_id>/like-comment/', views.like_comment, name='like_comment'),
    path('show-post/<int:post_id>/<int:comment_id>/delete-comment/', views.delete_comment, name='delete_comment'),
    
    # user_name cannot be 'register', 'login', 'logout', 'help', etc.
    path('<str:username>/', views.show_user, name='account'),
    path('<str:username>/folders/', views.all_folders, name='all_folders'),
    path('<str:username>/folders/add-folder/', views.add_folders, name='add_folders'),
    path('<str:username>/folders/<slug:folder_name_slug>/', views.show_folder, name='show_folder'),
    path('<str:username>/folders/<slug:folder_name_slug>/delete-folder/', views.delete_folder, name='delete_folder'),
    path('<str:username>/folders/<slug:folder_name_slug>/<int:post_id>/del-saved-post/', views.delete_saved_post,
         name='delete_saved_post'),
    path('<str:username>/my-attempts/', views.show_my_attempts, name='show_my_attempts'),
    path('<str:username>/my-posts/<int:post_id>/delete-post/', views.delete_post, name='delete_post'),
    path('<str:username>/update-profile/', views.update_profile,name='update_profile'),
    path('<str:username>/all-followed-categories/', views.all_followed_categories,name='all_followed_categories'),
    

    path('follow-user/<str:username>/', views.follow_user, name='follow_user'),
    path('follow-category/<slug:category_slug>/', views.follow_category, name='follow_category'),
    
    path('search/', views.search, name = 'search'),
    
    path('add-post-to-category/', views.add_post_to_category, name='add_post_to_category'),
    path('<slug:category_slug>/', views.show_category, name='show_category'),


]