
from multiprocessing import context
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from feed.models import Post, Folder, UserProfile, Likes, Category
from feed.models import Comment, Queries, Functions, FollowsUser, FollowsCategory, Categorises
from feed.forms import AddPostToFolderForm, UserPostsForm, UserForm, FolderForm, EditProfileForm, UserCommentForm, UserCreationForm, PostCategoryForm
from datetime import datetime


def home(request):
    # all posts uploaded to diTRY
    posts = Post.objects.all()
    visitor_cookie_handler(request)
    return render(request, 'feed/home.html', context={'posts': posts})

def about(request):
    return render(request, 'feed/about.html')


def help(request):
    return render(request, 'feed/help.html')


def contact_us(request):
    return render(request, 'feed/contact_us.html')


@login_required(login_url='feed:login')
def trending(request):
    # top ten posts with the most likes
    posts = Post.objects.order_by('-likes')[:10]
    return render(request, 'feed/categories.html', context={'posts':posts, 'name': 'Trending'})


@login_required(login_url='feed:login')
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


@login_required(login_url='feed:login')
def show_my_attempts(request,username):
    user = UserProfile.objects.get(username=username)
    my_attempts = Queries.get_user_attempts(user.id)
    return render(request, 'feed/attempts.html', {'posts': my_attempts, 'user': user})


@login_required
def add_post(request, original_id=None):
    # if it is an attempt, id of original is also an input argument

    user = UserProfile.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = UserPostsForm(request.POST)
        category_form = PostCategoryForm(request.POST)

        if form.is_valid() and category_form.is_valid():
            # add picture and user
            post = form.save(commit=False)
            post.creator = user
            if 'picture' in request.FILES:
                post.picture = request.FILES['picture']
            else:
                context = {'no_pic_error': 'You must include a picture.', 'form': form, 'category_form': category_form }
                return render(request, 'feed/addPost.html', context)    
            post.save()

            # categorise
            categorise = category_form.save(commit=False)
            categorise.post = post
            categorise.save()

            if original_id!=None:
                attempt_id = post.id
                # if it is an attempt redirect to show all attempts
                Functions.set_original(original_id, attempt_id)
                return redirect(reverse('feed:show_my_attempts', kwargs={'username':request.user.username}))

            post_id = post.id
            return redirect(reverse('feed:show_post', kwargs={'post_id':post_id}))
        else:
            # if form not valid print errors
            print(form.errors)
    else:
        form = UserPostsForm()
        category_form = PostCategoryForm()
    context = {'form':form, 'category_form': category_form}
    return render(request, 'feed/addPost.html',context)


@login_required(login_url='feed:login')
def show_post(request, post_id):

    form = UserCommentForm()
    context_dict = {}
    try:
        post = Post.objects.get(id = post_id)
        context_dict['post'] = post
        context_dict['creator'] = post.creator
        comments = Queries.get_comment_on_post(post.id)
        description = Queries.get_post_description(post.id)
        context_dict['description'] = description
        context_dict['comments'] = comments
        # liked by user?

        is_liked = Functions.has_liked(request.user.id,post_id)
        context_dict['is_liked'] = is_liked
        context_dict['form'] = form
   
    except Post.DoesNotExist:
        context_dict['post'] = None
        context_dict['comments'] = None
        context_dict['creator'] = None
        context_dict['numComments'] = 0
        context_dict['description'] = None
        context_dict['is_liked'] = False
        context_dict['form'] = None
    finally:
        return render(request, 'feed/picDetail.html', context = context_dict)


@login_required(login_url='feed:login')
def show_folder(request, folder_id, username):
    # maybe also need user_name to get folder
    context_dict = {}
    try:
        user = UserProfile.objects.get(username=username)
        folder = Folder.objects.get(id=folder_id, user=user)
        posts = Queries.get_posts_in_folder(folder_id)
        context_dict['username'] = user
        context_dict['folder']=folder
        context_dict['posts'] = posts

    except Folder.DoesNotExist:
        context_dict['username'] = None
        context_dict['folder'] = None
        context_dict['posts'] = None
    finally:
        # template show_folder.html does not exist yet, might have to change name
        return render(request, 'feed/show_folder.html',context=context_dict)


@login_required(login_url='feed:login')
def all_folders(request, user_folder):
    # helper function
    user = UserProfile.objects.get(id=request.user.id)
    if user == user_folder:
        folders=Folder.objects.filter(user=user_folder)
    else:
        folders=Folder.objects.filter(user=user_folder, private=False)

    return folders


@login_required(login_url='feed:login')
def show_user(request, username):
    show_user = UserProfile.objects.get(username=username)
    current_user = UserProfile.objects.get(id=request.user.id)
    cur_user = UserProfile.objects.get(username=request.user.username)

    context_dict = {}
    context_dict['user'] = show_user
    context_dict['cur_user'] = cur_user
    
    if show_user == current_user:
        #redirects to personal page
        posts = Queries.get_user_posts(show_user.id)
        followed_categories = Queries.get_category_following(request.user.id)
        folders = all_folders(request, show_user)

        context_dict = {'user':show_user, 'posts':posts, 'followed_categories':followed_categories, 'folders':folders}
        
        return render(request,'feed/personalPage.html', context=context_dict)

    else:
        # redirects to page of other user
        posts = Queries.get_user_posts(show_user.id)
        followed_categories = Queries.get_category_following(request.user.id)

        folders = all_folders(request, show_user)
        context_dict = {'user': current_user, 'show_user': show_user,'posts': posts, 'followed_categories': followed_categories, 'folders': folders}

        return render(request, 'feed/otherUserPage.html', context=context_dict)


@login_required(login_url='feed:login')
def show_category(request, name_category):
    posts = Queries.get_posts_in_category(name_category)

    return render(request, 'feed/categories.html', context={'posts':posts, 'name': name_category})


@login_required(login_url='feed:login')
def follow_user(request, username):
    following_user = UserProfile.objects.get(id = request.user.id)
    follow_user = UserProfile.objects.get(username=username)

    if FollowsUser.objects.filter(follower=following_user, following= follow_user).exists():
        FollowsUser.objects.get(follower=following_user, following= follow_user).delete()
    else:
        FollowsUser.objects.get_or_create(follower=following_user, following=follow_user)

    return redirect(reverse('feed:account', kwargs={'username':username}))


@login_required(login_url='feed:login')
def add_folder(request,username):
    form = FolderForm()
    add_folder_user = UserProfile.objects.get(username=username)
    current_user = UserProfile.objects.get(username=request.user.username)
    # can only add folder for own account
    if current_user == add_folder_user:
        # tests if HTTP POST
        if request.method == 'POST':
            form = FolderForm(request.POST)

            if form.is_valid():
                # Saves new folder to the database.
                folder = form.save(commit=False)
                folder.user = current_user
                folder.save()
            else:
                print(form.errors)

        return render(request, 'feed/add_folder.html', context={'form':form })

    else:
        return redirect(reverse('feed:account', kwargs={'username':username}))


@login_required(login_url='feed:login')
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


@login_required(login_url='feed:login')
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
@login_required(login_url='feed:login')
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


@login_required(login_url='feed:login')
def comment_on_post(request, post_id):
    if request.method == 'POST':
        form = UserCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post_id
            comment.user_id = request.user.id
            comment.save()

        else:
            print(form.errors)
    return redirect(reverse('feed:show_post',
                            kwargs={'post_id': post_id}))



@login_required(login_url='feed:login')
def search_title(request):
    # for reference:
    #https://stackoverflow.com/questions/38006125/how-to-implement-search-function-in-django
    if request.method == 'GET':
        # gets all search terms
        query= request.GET.get('Search')
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
                  context={'matching_posts': matching_posts, 'query': query})


@login_required(login_url='feed:login')
def update_profile(request,username):
    update_user = UserProfile.objects.get(username=username)
    current_user = UserProfile.objects.get(username=request.user.username)
    form = EditProfileForm()

    if update_user == current_user:
        if request.method == 'POST':
           form = EditProfileForm(request.POST, request.FILES,instance=current_user)
           if form.is_valid():
               form.save()
               return redirect(reverse('feed:account', kwargs={'username':current_user.username}))

        
        return render(request, 'feed/updateProfile.html', context={'form':form})

    else:
        # cannot update someone elses profile thus gets redirected to his own profile
        return redirect(reverse('feed:account', kwargs={'username':current_user.username}))


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
@login_required(login_url='feed:login')
def userFollowing(request):
    cur_user = UserProfile.objects.get(username=request.user.username)
    get_following = Queries.get_user_following(user=cur_user.id)
    context = {}
    context['following'] = get_following

    return render(request,'feed/userFollowing.html',context)


@login_required(login_url='feed:login')
def userFollowers(request):
    cur_user = UserProfile.objects.get(username=request.user.username)
    get_followers = Queries.get_user_follows(user=cur_user.id)
    context = {}
    context['followers'] = get_followers
    return render(request,'feed/userFollower.html',context)


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('feed:home'))


def add_post_to_folder(request,post_id):

    if request.method == 'POST':
        post_object = Post.objects.get(id=post_id)
        form = AddPostToFolderForm(request.user,request.POST)

        if form.is_valid():
         
            object = form.save(commit=False)
            
            object.post = post_object
            object.save()
            return redirect(reverse('feed:show_folder', kwargs={'username':request.user.username,'folder_id':object.folder.id}))
        else:
            
            print(form.errors)
    else:
        post_object = Post.objects.get(id=post_id)
        form = AddPostToFolderForm(request.user)

    context_dict = {}
    try:
        post = Post.objects.get(id = post_id)
        context_dict['post'] = post
        context_dict['creator'] = post.creator
        description = Queries.get_post_description(post.id)
        context_dict['description'] = description
        context_dict['form'] = form
        # liked by user?
        
        is_liked = Functions.has_liked(request.user.id,post_id)
        context_dict['is_liked'] = is_liked
        

    except Post.DoesNotExist:
        context_dict['post'] = None
        context_dict['comments'] = None
        context_dict['creator'] = None
        context_dict['numComments'] = 0
        context_dict['description'] = None
        context_dict['is_liked'] = False
        context_dict['form'] = None
        
    finally:
        
        return render(request,'feed/add_to_folder.html',context_dict)    


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

def get_home_likes(request):
    
    if(request.is_ajax()):
        user = request.POST.get('user')#
        likes = Queries.get_liked_posts(user)
        data = list()
        if likes != None:
            for like in likes:
                data.append(like.id)
        return JsonResponse({'data':data})
    return JsonResponse({})


def get_follows(request):
    if(request.is_ajax()):
        user = request.POST.get('user')
        other_user = request.POST.get('other_user')
        followed = Queries.get_user_following(user)
        print(followed)
        
        is_following = followed.filter(id = other_user)
        if(is_following != None):
            if is_following.count()>0:
                return JsonResponse({'followed':True})
            else:
                return JsonResponse({'followed':False})
        else:
            return JsonResponse({'followed':False})
    return JsonResponse({})

