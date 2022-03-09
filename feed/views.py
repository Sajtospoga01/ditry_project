
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from feed.models import Post, Folder, UserProfile, Like
from feed.models import Comment, Queries, Functions, FollowsUser, FollowsCategory, Categorises
from feed.forms import PostForm, UserForm, FolderForm
from datetime from datetime

# FolderForm does not exist yet

def home(request):
    # all posts uploaded to diTRY
    ## should posts maybe just be pictures 
    posts = Post.objects.all()
    visitor_cookie_handler(request)
    context_dict = {'posts': posts}
    return render(request, 'feed_templates/home.html', context=context_dict)



def about(request):
    return render(request,'feed_templates/about.html')


def help(request):
    return render(request,'feed_templates/help.html')


def contact_us(request):
    return render(request,'feed_templates/contact.html')


@login_required
def trending(request):
    # top ten posts with the most likes
    posts = Post.objects.order_by('-likes')[:10]
    return render(request, 'feed_templates/trending.html', context={'posts'=posts})


@login_required
def follow_category(request, category_name_slug):
    # user follows category and is redirected to this category
    following_user = request.user
    follows_category = Category.objects.get(slug=category_name_slug)

    if FollowsCategory.objects.filter(follower=following_user, following=follows_category).exists():
        # if user already follows category, clicking on follow again, makes user unfollow category
        FollowsCategory.objects.filter(follower=following_user, following=follows_category).delete()
    else:
        FollowsCategory.objects.filter(follower=following_user, following=follows_category).save()

    return redirect(reverse('feed:show_category', kwargs={'category_slug': category_name_slug}))



@login_required
def show_my_posts(request, user_name):
    ### might have to be changed if separate model for my_posts
    posts = Queries.get_user_posts(user_name)
    return render(request, 'feed_templates/show_my_posts.html', context ={'posts':posts})


@login_required
def show_my_attempts(request,user_name):
    #... uses my_attempts model
    return


@login_required
def add_post(request):
    # post should be automatically added to 'my posts'

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            post_id = post.id

            return redirect(reverse('feed:show_post', kwargs={'post_id':post_id}))
        else:
            # if form not valid print errors
            print(form.errors)
            
    # might have to add kwargs={'user_id':user_id}
    return redirect(reverse('feed:my_account'))

@login_required
def add_post_to_category(request, category_slug, post_id):
    post = Post.objects.get(id = post_id)
    category = Category.objects.get(slug=category_name_slug)
    # post is added to category
    Functions.connect_post_to_category(post, category).save()
    return redirect(reverse('feed:show_category'))


@login_required
def show_post(request, post_id):
    context_dict= {}
    try:
        post = Post.objects.get(id = post_id)
        context_dict['post'] = post
        context_dict['likes'] = post.likes
        # maybe also show comments associated with posts
    except Post.DoesNotExist:
        context_dict['post'] = None

    return render(request, 'feed_templates/post.html', context = context_dict)

@login_required
def show_folder(request, folder_name_slug):
    # maybe also need user_id to get folder
    context_dict={}
    try:
        folder = Folder.objects.get(slug=folder_name_slug)
        posts = Post.objects.filter(folder=folder)
        context_dict['folder']=folder
        context_dict['posts'] = posts

    except Folder.DoesNotExist:
        context_dict['folder'] = None
        context_dict['posts'] = None

    # template show_folder.html does not exist yet, might have to change name
    return render(request, 'feed_templates/show_folder.html',context=context_dict)

@login_required
def all_folders(request, user_id):
    # returns all folders that a user account has
    return

@login_required
def show_user(request, user_name):
    # should return user and user_name
    user = UserProfile.objects.get(username=user_name)
    return

@login_required
def all_followed_category(request):
    # returns categories that a user follows
    return

@login_required
def show_category(request, category_id):
    posts = Queries.get_posts_in_category(category_id)
    return render(request, 'feed_templates/show_category.html', context ={'posts':posts})



@login_required
def helper_delete_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()


@login_required
def delete_saved_post(request, post_id, folder_name_slug):
    helper_delete_post(request,post_id)
    return redirect(reverse('feed:show_folder',
                                        kwargs={'folder_name_slug':
                                                folder_name_slug}))

@login_required
def delete_post(request, post_id):
    helper_delete_post(request, post_id)
    return redirect(reverse('feed:show_folder',
                                        kwargs={'folder_name_slug':
                                                folder_name_slug}))


@login_required
def delete_folder(request, folder_id):
    folder = get_object_or_404(Post, id=folder_id)
    if request.method == 'POST':
        folder.delete()
    return redirect(reverse('feed:my_account'))


@login_required
def follow_user(request, user_name):
    following_user = request.user
    follow_user = UserProfile.objects.get(username=user_name)

    if FollowsUser.objects.filter(follower=following_user, following= follow_user).exists():
        FollowsUser.objects.filter(follower=following_user, following= follow_user).delete()
    else:
        FollowsUser.objects.filter(follower=following_user, following=follow_user).save()

    return redirect(reverse('feed:show_user', kwargs={'user_id':user_id}))


@login_required
def add_folder(request):
    form = FolderForm()

    # tests if HTTP POST
    if request.method == 'POST':
        form = FolderForm(request.POST)

        if form.is_valid():
            # Saves new folder to the database.
            form.save(commit=True)
            return redirect(reverse('feed:my_account'))
        
        else:
            print(form.errors)

    return render(request, 'feed_templates/add_folder.html', {'form': form})

@login_required
def like_post(request,post_id):
    # reference: https://github.com/Jebaseelanravi/instagram-clone/blob/main/insta/views.py
    post = Post.objects.get(id= post_id)

    try:
        already_Liked = Likes.objects.get(liked_post=post, liker=request.user)
        Likes.objects.filter(liked_post=post, liker=request.user).delete()
        post.likes -= 1

    except Like.DoesNotExist:
        Likes.objects.create(liked_post=post, liker=request.user)
        post.likes += 1

    post.save()
    #should redirect to post that was liked or disliked
    return redirect(reverse('feed:home'))

@login_required
def save_post(request, folder_name_slug ,post_id):

    try:
        folder = Folder.objects.get(slug=folder_name_slug)
    except Folder.DoesNotExist:
        folder = None

    # Cannot add post into none existing folder
    if folder is None:
        return redirect(reverse('feed:my_account'))

    if request.method == 'POST':
        pin = get_object_or_404(Post, post_id)
        form = PostForm(request.POST)

        if form.is_valid():
            if folder:
                saved_post = form.save(commit=False)
                saved_post.likes = pin.likes
                saved_post.title = pin.title

                # folder currently not in model, how to save in specific folder?
                saved_post.folder = folder
                saved_post.save()

                return redirect(reverse('feed:my_account'))
        else:
            print(form.errors)

    context_dict = {'form': form, 'folder': folder}
    return render(request, 'feed_templates/add_post.html', context=context_dict)


@login_required
def like_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)

    try:
        # name of comment_likes class might have to  be changed
        already_Liked = Comment_likes.objects.get(liked_comment=comment, liker=request.user)
        Likes.objects.filter(liked_post=post, liker=request.user).delete()
        comment.likes -= 1

    except Like.DoesNotExist:
        # name of comment_likes class might have to  be changed
        Comment_likes.objects.create(liked_post=post, liker=request.user)
        comment.likes += 1

    comment.save()
    # should redirect to post on which comment was liked or disliked
    return redirect(reverse('feed:home'))

@login_required
def comment_on_post(request, post_id):
    #...
    return

@login_required
def show_comments_on_post(request, post_id):
    #...
    return

@login_required
def delete_comment(request, comment_id):
    try:
        this_comment = Comment.objects.get(id=comment_id, user_id=request.user)
        Comment.objects.filter(id=comment_id, user_id=request.user).delete()
        post_id = this_comment.post_id
        return redirect(reverse('feed:show_post', kwargs={'post_id':post_id}))
    except this_comment.DoesNotExist:
        # might have to insert kwargs with request.user
        return redirect(reverse('feed:my_account'))


@login_required
def search(request):
    # for reference:
    #https://stackoverflow.com/questions/38006125/how-to-implement-search-function-in-django
    if request.method == 'GET':
        # gets all search terms
        queries = request.GET['q'].split()
        all_posts = Post.objects.all()
        matching_posts = []
        # loops through all search terms
        for query in queries:
            if query is not None:
                # filters post by if search term in title
                for p in all_posts.filter(Q(title__icontains = query)):
                    if p not in matching posts:
                        matching_posts.append(p)


    return render(request,'feed_templates/search.html', {'matching_posts': matching_posts})

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid() :
            user = user_form.save()

            user.set_password(user.password)

            if 'picture' in request.FILES:
                user.profile_picture = request.FILES['picture']
            user.save()
            registered = True
            
        else:
            print(user_form.errors, )
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request,
                  'register/register.html',
                  context = {'user_form': user_form,
                             'registered': registered})

@login_required
def update_profile(request):
   if request.method=='POST':
       form = EditProfileForm(request.POST)
       if form.is_valid:
           form.save()
    #update_profile does no exist yet, might have to change name
    return render(request, 'register/update_profile.html', context={'user_form':form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('feed:home'))
            else:
                # inactive account
                return HttpResponse("Your diTry account is disabled.")
        else:
            # invalid login details
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'registration/login.html')


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



