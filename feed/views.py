
from multiprocessing import context
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from django.conf.urls.static import static
from feed.models import Post, Folder, UserProfile, Likes, Category
from feed.models import Comment, Queries, Functions, FollowsUser, FollowsCategory, Categorises
from feed.forms import UserPostsForm, UserForm, FolderForm, EditProfileForm, UserCommentForm, UserCreationForm, UserProfileForm
from feed.forms import ResetForm
from datetime import datetime



def home(request):
    # all posts uploaded to diTRY
    posts = Post.objects.all()
    visitor_cookie_handler(request)
    context_dict = {'posts': list()}
    index = 0
    row = -1
    for i in posts:
        if index % 3 == 0:
            row += 1
            context_dict['posts'].append(list())
        context_dict['posts'][row].append(i)
        index += 1

    return render(request, 'feed/home.html', context=context_dict)


def about(request):
    return render(request,'feed/about.html' )


def help(request):
    return render(request,'feed/help.html')


def contact_us(request):
    return render(request,'feed/contact_us.html')


@login_required
def trending(request):
    # top ten posts with the most likes
    posts = Post.objects.order_by('-likes')[:10]
    return render(request, 'feed/categories.html', context={'posts':posts, 'name': 'Trending'})


@login_required
def follow_category(request, category_name_slug):
    # user follows category and is redirected to this category
    following_user = UserProfile.objects.get(id = request.user.id)
    follows_category = Categorises.objects.get(slug=category_name_slug)

    if FollowsCategory.objects.filter(follower=following_user, following=follows_category).exists():
        # if user already follows category, clicking on follow again, makes user unfollow category
        FollowsCategory.objects.filter(follower=following_user, following=follows_category).delete()
    else:
        FollowsCategory.objects.filter(follower=following_user, following=follows_category).save()

    return redirect(reverse('feed:show_category', kwargs={'category_slug': category_name_slug}))


@login_required
def show_my_attempts(request):
    user = UserProfile.objects.get(id = request.user.id)
    my_attempts = Post.objects.filter(creator=user, original__isnull=False)
    return render(request, 'attempts.html',context={'attempts':my_attempts})


@login_required
def add_post(request, boolean_attempt, attempt_post_id=None):
    # boolean_attempt is True if user posts an attempt, otherwise False if original post
    # if it is an attempt, id of original is also an input argument

    user = UserProfile.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = UserPostsForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.creator = user
            if 'picture' in request.FILES:
                post.picture = request.FILES['picture']
            post.save()
            if boolean_attempt!=0 and attempt_post_id!=None:
                attempt_id = post.id
                # if it is an attempt redirect to show all attempts
                Functions.set_original(attempt_post_id, attempt_id)
                return redirect(reverse('feed:show_my_attempts', kwargs={'username':request.user.username}))

            post_id = post.id
            return redirect(reverse('feed:show_post', kwargs={'post_id':post_id}))
        else:
            # if form not valid print errors
            print(form.errors)
    else:
        form = UserPostsForm()
    context = {'form':form}
    return render(request, 'feed/addPost.html',context)

@login_required
def add_post_to_category(request, category_name_slug, post_id):
    post = Post.objects.get(id = post_id)
    category = Categorises.objects.get(slug=category_name_slug)
    # post is added to category
    Functions.connect_post_to_category(post, category)
    return redirect(reverse('feed:show_category',kwargs={'category_slug': category_name_slug}))



#helper function
def has_liked(request, post):
    user = UserProfile.objects.get(username=request.user.username)
    liked = Queries.get_liked_posts(user)
    result = liked.objects.filter(id=post.id)
    if result.count()>0:
        return True
    else:
        return False

@login_required
def show_post(request, post_id):
    context_dict = {}
    try:
        post = Post.objects.get(id = post_id)
        context_dict['post'] = post
        context_dict['creator'] = post.creator
        comments = Queries.get_comment_on_post(post.id)
        context_dict['comments'] = comments
        # liked by user?
        
        is_liked = Functions.has_liked(request.user.username,post_id)
        context_dict['is_liked'] = is_liked
   
    except Post.DoesNotExist:
        context_dict['post'] = None
        context_dict['comments'] = None
        context_dict['creator'] = None
        context_dict['numComments'] = 0
        context_dict['is_liked'] = False
    finally:
        return render(request, 'feed/picDetail.html', context = context_dict)


@login_required
def show_folder(request, folder_id, username):
    # maybe also need user_name to get folder
    context_dict = {}
    try:
        user = UserProfile.objects.get(username=username)
        folder = Folder.objects.get(id=folder_id, user=user)
        posts = Queries.get_posts_in_folder(folder_id)
        context_dict['folder']=folder
        context_dict['posts'] = posts

    except Folder.DoesNotExist:
        context_dict['folder'] = None
        context_dict['posts'] = None
    finally:
        # template show_folder.html does not exist yet, might have to change name
        return render(request, 'feed/show_folder.html',context=context_dict)


@login_required
def all_folders(request, user_folder):
    # helper function
    user = UserProfile.objects.get(id=request.user.id)
    if user == user_folder:
        folders=Folder.objects.filter(user=user_folder)
    else:
        folders=Folder.objects.filter(user=user_folder, private=False)

    return folders


@login_required
def show_user(request, username):
    user = UserProfile.objects.get(username=username)
    posts = Queries.get_user_posts(username)
    followed_categories = Queries.get_category_following(request.user.id)

    folders = all_folders(request, user)
    context_dict = {'user':user, 'posts':posts, 'followed_categories':followed_categories, 'folders':folders}

    return render(request,'feed/personalPage.html', context=context_dict)



@login_required
def all_followed_users(request):
    follows = Queries.get_user_following(request.user.id)
    ## also needs sepaparate url if not helper function to display on personal page
    return

@login_required
def show_category(request, name_category):
    posts = Queries.get_posts_in_category(name_category)

    return render(request, 'feed/categories.html', context={'posts':posts, 'name': name_category})

# def show_category_helper( category_name):
#     category = Category.objects.get(name=category_name)
#     category_id = category.id
#     posts = Queries.get_posts_in_category(category_id)
#     return category, posts
#
# @login_required
# def crafts(request, category_id):
#     category, posts = show_category_helper(category_id)
#     return render(request, 'feed/crafts.html', context={'posts':posts, 'category':category})
#
# @login_required
# def diys(request, category_id):
#     category, posts = show_category_helper(category_id)
#     return render(request, 'feed/diys.html', context={'posts':posts, 'category':category})
#
#
# @login_required
# def food(request, category_id):
#     category, posts = show_category_helper(category_id)
#     return render(request, 'feed/food.html', context={'posts':posts, 'category':category})
#
# @login_required
# def crafts(request):
#     category, posts = show_category_helper("Craft")
#     return render(request, 'feed/crafts.html', context={'posts':posts, 'category':category})
#
# @login_required
# def diys(request):
#     category, posts = show_category_helper("Diy")
#     return render(request, 'feed/diys.html', context={'posts':posts, 'category':category})
#
#
# @login_required
# def food(request):
#     category, posts = show_category_helper("Cook")
#     return render(request, 'feed/food.html', context={'posts':posts, 'category':category})


def helper_delete_post(request,post):
    if request.method == 'POST':
        post.delete()


@login_required
def delete_saved_post(request, post_id, folder_id):
    # needs to check if post in specific folder and if folder by request.user
    post = get_object_or_404(Post, id=post_id)
    helper_delete_post(request,post)
    return redirect(reverse('feed:show_folder',
                                        kwargs={'folder_id':
                                                folder_id, 'username':request.user.username}))


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = UserProfile.objects.get(id = request.user.id)
    if post.creator == user:
        helper_delete_post(request, post)
    return redirect(reverse('feed:account',kwargs={'username':request.user.username}))


@login_required
def delete_folder(request, folder_id):
    folder = get_object_or_404(Post, id=folder_id)
    if request.method == 'POST':
        folder.delete()
    return redirect(reverse('feed:account',kwargs={'username':request.user.username}))


@login_required
def follow_user(request, username):
    following_user = UserProfile.objects.get(id = request.user.id)
    follow_user = UserProfile.objects.get(username=username)
    

    if FollowsUser.objects.filter(follower=following_user, following= follow_user).exists():
        FollowsUser.objects.get(follower=following_user, following= follow_user).delete()
    else:
        FollowsUser.objects.get_or_create(follower=following_user, following=follow_user)

    return redirect(reverse('feed:account', kwargs={'username':username}))


@login_required
def add_folder(request):
    form = FolderForm()

    # tests if HTTP POST
    if request.method == 'POST':
        form = FolderForm(request.POST)

        if form.is_valid():
            # Saves new folder to the database.
            form.save()
            return redirect(reverse('feed:all_folders',kwargs={'username':request.user.username}))
        
        else:
            print(form.errors)

    return render(request, 'feed/add_folder.html', context={'form': form})


@login_required
def like_post(request,post_id):
    # reference: https://github.com/Jebaseelanravi/instagram-clone/blob/main/insta/views.py
    post = Post.objects.get(id= post_id)
    liker = UserProfile.objects.get(id=request.user.id)
    try:
        already_Liked = Likes.objects.get(liked_post=post, liker=liker)
        Likes.objects.filter(liked_post=post, liker=liker).delete()

        if post.likes>0:
            post.likes -= 1

    except Likes.DoesNotExist:
        Likes.objects.create(liked_post=post, liker=liker)
        post.likes += 1

    finally:
        post.save()
        # should redirect to post that was liked or disliked
        return redirect(reverse('feed:show_post', kwargs={'post_id':post_id}))


@login_required
def save_post(request, folder_id ,post_id):
    try:
        folder = Folder.objects.get(slug=folder_id)
    except Folder.DoesNotExist:
        folder = None
    finally:
        # Cannot add post into none existing folder
        if folder is None:
            return redirect(reverse('feed:account',kwargs={'username':request.user.username}))

        form = UserPostsForm()
        if request.method == 'POST':
            pin = get_object_or_404(Post, post_id)
            form = UserPostsForm(request.POST)

            if form.is_valid():
                if folder:
                    saved_post = form.save(commit=False)
                    saved_post.likes = pin.likes
                    saved_post.title = pin.title
                    saved_post.creator = pin.creator

                    # folder currently not in model, how to save in specific folder?
                    saved_post.folder = folder
                    saved_post.save()

                    return redirect(reverse('feed:show_user',
                                            kwargs={'username':request.user.username,'folder_id':folder_id}))
            else:
                print(form.errors)

        context_dict = {'form': form, 'folder': folder}
        return render(request, 'feed/addPost.html', context=context_dict)

# might not need this view, if not needed also delete url for it
@login_required
def like_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post_id = comment.post_id
    liker = UserProfile.objects.get(id=request.user.id)

    try:
        # name of comment_likes class might have to  be changed
        already_Liked = Likes.objects.get(liked_comment=comment, liker=liker)
        Likes.objects.filter(liked_post=Post, liker=request.user).delete()
        comment.likes -= 1

    except Likes.DoesNotExist:
        # name of comment_likes class might have to  be changed
        Likes.objects.create(liked_post=Post, liker=liker)
        comment.likes += 1
    finally:
        comment.save()
        return redirect(reverse('feed:show_comments_on_post', kwargs={'post_id':post_id}))


@login_required
def comment_on_post(request, post_id):
    if request.medthod == 'POST':
        form = UserCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post_id
            comment.user_id = request.user.id
            comment.save()
            return redirect(reverse('feed:show_comments_on_post',
                                    kwargs={'post_id': post_id}))

        else:
            print(form.errors)
    return redirect(reverse('feed:show_post',
                            kwargs={'post_id': post_id}))


@login_required
def delete_comment(request, comment_id):
    try:
        user = UserProfile.objects.get(id=request.user.id)
        this_comment = Comment.objects.get(id=comment_id, user_id=user)
        Comment.objects.filter(id=comment_id, user_id=user).delete()
        post_id = this_comment.post_id
        return redirect(reverse('feed:show_post', kwargs={'post_id':post_id}))
    except Comment.DoesNotExist:
        return redirect(reverse('feed:account',kwargs={'username':request.user.username}))


@login_required
def search_title(request):
    # for reference:
    #https://stackoverflow.com/questions/38006125/how-to-implement-search-function-in-django
    if request.method == 'GET':
        # gets all search terms
        query= request.GET.get('q')
        queries =query.split()
        all_posts = Post.objects.all()
        matching_posts = []

        # loops through all search terms
        for query in queries:
            if query is not None:

                # filters post by if search term in title
                for p in all_posts.filter(Q(title__icontains = query)):
                    if p not in matching_posts:
                        matching_posts.append(p)

    return render(request,'feed/searchTitle.html',
                  context={'matching_posts': matching_posts})

@login_required
def update_profile(request,username):
   form = EditProfileForm()
   if request.method == 'POST':
       form = EditProfileForm(request.POST)

       if form.is_valid:
           form.save()
           return redirect(reverse('feed:account', kwargs={'username':request.user.username}))

   #update_profile does not exist yet, might have to change name
   return render(request, 'register/update_profile.html', context={'user_form':form})


def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('feed:login')
    context = {'form':form}

    return render(request,'feed/register.html',context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
                login(request, user)
                return redirect(reverse('feed:home'))
        else:
            # invalid login details
            messages.info(request,'Username or Password is incorrect')
    context = {}
    return render(request, 'feed/login.html',context)


# queries exist for this, this is just a bandaid solution
@login_required
def userFollowing(request):
    get_following = FollowsUser.objects.get('following')
    get_cat_following = FollowsCategory.objects.get('following')
    
    context = {}
    context['followers'] = get_following
    context['topics'] = get_cat_following

    return render(request,'feed/userFollowing.html',context)

@login_required
def userFollowers(request):
    get_followers = FollowsUser.objects.get('follower')
    context = {}
    context['followers'] = get_followers
    return render(request,'feed/userFollower.html',context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('feed:home'))


# helper function
def get_server_side_cookie(request,cookie,default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    # number of visits to website with default value 1
    visits = int((get_server_side_cookie(request,'visits', '1')))

    last_visit_cookie = get_server_side_cookie(request,'last_visit',
                                            str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    # If it has been more than an hour since the last visit...
    if(datetime.now()-last_visit_time).seconds > 3600:
        visits = visits + 1
        # Update the last visit cookie after having updated the count
        request.session['last_visit'] = str(datetime.now())

    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/ set the visits cookie
    request.session['visits'] = visits



