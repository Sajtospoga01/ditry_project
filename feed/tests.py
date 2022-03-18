import os
import warnings
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

from feed.models import *
from django.contrib.auth.models import User
from django.core.files.images import ImageFile

# some maybe unnecessary project structure tests, might be added to

class ProjectStructureTests(TestCase):

    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.feed_app_dir = os.path.join(self.project_base_dir, 'feed')

    def test_feed_app_configured(self):
        is_app_configured = 'feed' in settings.INSTALLED_APPS

        self.assertTrue(is_app_configured, f"Feed app missing from INSTALLED_APPS in settings.py")

# all views tests, incredibly incomplete

class HomePageTest(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('feed.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('ditry_project.urls')

    def test_view_exists(self):
        name_exists = 'home' in self.views_module_listing
        is_callable = callable(self.views_module.index)

        self.assertTrue(name_exists, f"The home() view does not exist.")
        self.assertTrue(is_callable, f"home() view is not a function")

    def test_mappings_exists(self):
        home_mapping_exists = False

        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'home':
                    home_mapping_exists = True

        self.assertTrue(home_mapping_exists, f"The home url mapping could not be found.")
        self.assertEqual(reverse('feed:home'), '/home/', f"home url lookup failed.")

    def test_home_view_with_no_posts(self):
        response = self.client.get(reverse('feed:home'))

        self.assertEqual(response.status_code, 200, f"Home page not returned with status code 200.")
        self.assertContains(response, 'Feed empty.', f"'Feed empty.' message not displayed.") ## not implemented
        self.assertQuerysetEqual(response.context['posts'], [], f" Non-empty posts context.") ## also not checked

    def test_home_view_with_posts(self):
        # add post
        #and again and again
        response = self.client.get(reverse('feed:home'))
        self.assertEqual(response.status_code, 200,f"Home page not returned with status code 200.")
        self.assertContains() # a couple these
        num_posts = len(response.context['posts'])
        self.assertEqual(num_posts, 3, f"Wrong number of posts passed in response.")

# all database related tests, getting there

class DatabaseConfigurationTests(TestCase):
    def test_databases_variable_exists(self):
        self.assertTrue(settings.DATABASES, f"Settings module doesn't have a DATABASE variable.")
        self.assertTrue('default' in settings.DATABASES, f"No default database configuration.")


class ModelTests(TestCase):
    def setUp(self):
        Helper.create_model_setup()

    def test_category_model(self):
        c_diy = Category.objects.get(name = "diy")
        self.assertTrue(c_diy.id>=0, f"Category id not autofilled.")
        c_food = Category.objects.get(name = "food")
        self.assertTrue(c_food.id > c_diy.id, f"Category id doesn't increment.")

    def test_category_slug(self):
        pass

    def test_post_model(self):
        post = Post.objects.get(id = 1)
        self.assertEqual(post.title, "test", f"Expected title test, got {post.title}.")
        self.assertEqual(post.creator, User.objects.get(username = "alicej"), f"Unexpected creator.")

    def test_str_methods(self):
        category_diy = Category.objects.get(name='diy')
        user_alice = User.objects.get(username = "alicej")
        test_post = Post.objects.get(id=1)
        test_comment = Comment.objects.get(id = 1)

        self.assertEqual(str(category_diy), "diy", f"Category string method doesn't work. Expected 'diy' and got '{str(category_diy)}'.")
        self.assertEqual(str(user_alice), "alicej1", f"UserProfile string method doesn't work. Expected 'alicej1' and got '{str(user_alice)}'.")
        self.assertEqual(str(test_post), "test", f"Post string method doesn't work. Expected 'test' and got '{str(test_post)}'.")
        self.assertEqual(str(test_comment), "test comment", f"Comment string method doesn't work. Expected 'test comment' and got '{str(test_comment)}'.")

    def test_likes_are_positive(self):
        p = Post.objects.create(creator = User.objects.get(username = "alicej"),title = "likes_test",likes = -1)
        p.picture.save("sample_2.jpg", ImageFile(open("sample_images/sample_2.jpg","rb")))
        self.assertTrue((p.likes >= 0), f"Post likes should not be negative.")
    
class UniqueConstraintTests(TestCase):
    def setUp(self):
        pass
    def test_comment_unique(self):
        pass
    def test_followsuser_unique(self):
        pass
    def test_followscategory_unique(self):
        pass
    def test_like_unique(self):
        pass
    def test_categorises_unique(self):
        pass
    def test_folder_unique(self):
        pass

class QueryTests(TestCase):
    def setUp(self):
        Helper.create_model_setup()

    def test_get_comment_on_post(self):
        comments = Queries.get_comment_on_post(1)
        self.assertEqual(len(comments), 2, f"Expected 2 comments, found {len(comments)}.")
        self.assertContains(comments, Comment.objects.get(comment = "test comment"), f"Expected to find 'test comment' in comments.")

    def test_get_original(self):
        original = Queries.get_original(2)
        self.assertEqual(original.id, 1, f"Original post expected to have id 1, has id {original.id}.")

    def test_get_attempts(self):
        attempts = Queries.get_attempts(1)
        self.assertEqual(len(attempts), 1, f"Expected 1 attempt, found {len(attempts)}.")
        self.assertContains(attempts, Post.objects.get(id = 2), f"Expected post with id 2 to be in attempts of post 1.")

    def test_get_liked_posts(self):
        liked_posts = Queries.get_liked_posts(1)
        self.assertEqual(len(liked_posts),2, f"Expected user 1 to have liked 2 posts.")
        self.assertContains(liked_posts, Post.objects.get(id=2), f"Expected post 2 in user one's liked posts.")

    def test_get_post_likes(self):
        post_likes = Queries.get_post_likes(1)
        self.assertEqual(len(post_likes),2, f"Expected post 1 to have 2 likes.")
        self.assertContains(post_likes, User.objects.get(username="bobs"), f"Expected post 1 to be liked by user bobs.")

    def test_get_category_following(self):
        category_following = Queries.get_category_following(1)
        self.assertEqual(len(category_following), 2, f"Expected user 1 to follow 2 categories.")
        self.assertContains(category_following, Category.objects.get(name="diy"), f"Expected user 1 to be following the diy category.")

    def test_get_category_follows(self):
        follows_category = Queries.get_category_follows(1)
        self.assertEqual(len(follows_category), 2, f"Expected two users to be following category 1.")
        self.assertContains(follows_category, User.objects.get(username = "alicej"), "Expected alicej to be following category 1.")

    def test_get_posts_in_category(self):
        posts_in_category = Queries.get_posts_in_category(1)
        self.assertEqual(len(posts_in_category), 2, f"Expected two posts in category 1.")
        self.assertContains(posts_in_category, Post.objects.get(id = 1), "Expected post 1 to be in category 1.")

    def test_get_category_of_post(self):
        category = Queries.get_category_of_post(1)
        self.assertEqual(category[0], Category.objects.get(id=1), f"Expected query to return category 1.")
    
    def test_get_user_posts(self):
        posts = Queries.get_user_posts(1)
        self.assertEqual(posts[0], Post.objects.get(id =1), f"Expected query to return post 1.")

    def test_get_user_following(self):
        following = Queries.get_user_following(2)
        self.assertEqual(following[0], User.objects.get(username = "alicej"), f"Query expected to return user alicej.")

    def test_get_user_follows(self):
        followers = Queries.get_user_follows(1)
        self.assertEqual(followers[0], User.objects.get(username = "bobs"), f"Expected query to return user bobs.")
        followers = Queries.get_user_follows(2)
        self.assertEqual(len(followers), 0, f"Expected query to return empty list.")
    
    def test_get_posts_in_folder(self):
        posts = Queries.get_posts_in_folder(1)
        self.assertEqual(len(posts), 1, f"Expected query to return only 1 post.")
        self.assertContains(posts, Post.objects.get(id = 1), f"Expected query to return post 1.")
    
    def test_get_user_folders(self):
        folders = Queries.get_user_folders(1)
        self.assertEqual(len(folders), 1, f"Expected query to return only 1 folder.")
        self.assertContains(folders, Folder.objects.get(id = 1), f"Expected query to return folder 1.")


# tests for the population script, done except one
class PopulationScriptTests(TestCase):
    def setUp(self):
        try:
            import populate_feed
        except ImportError:
            raise ImportError(f"Could not import population script.")
        
        if 'populate' not in dir(populate_feed):
            raise NameError(f"The populate() function does not exist in the populate_feed module.")

        populate_feed.populate()

    def test_categories(self):
        categories = Category.objects.filter()
        categories_len = len(categories)
        categories_strs = map(str, categories)
        
        self.assertEqual(categories_len, 3, f"Expecting 3 categories to be created from the populate_feed module; found {categories_len}.")
        self.assertTrue('Craft' in categories_strs, f"The category 'Craft' was expected but not created by populate_feed.")
        self.assertTrue('Diy' in categories_strs, f"The category 'Diy' was expected but not created by populate_feed.")
        self.assertTrue('Cook' in categories_strs, f"The category 'Cook' was expected but not created by populate_feed.")

    def test_posts(self):
        exp_posts = {'title1': {'id':1,'picture':'sample_1.jpg','creator':1,'likes':0},
                    'title2': {'id':2,'picture':'sample_2.jpg','creator':1,'likes':0},
                    'title3': {'id':3,'picture':'sample_3.jpg','creator':1,'likes':0}}
        posts = Post.objects.filter()
        self.assertEqual(len(posts), len(exp_posts), f" Expected {len(exp_posts)} but got {len(posts)}.")

        for post in exp_posts:
            try:
                p = Post.objects.get(id=exp_posts[post]["id"])
            except Post.DoesNotExist:
                raise ValueError(f"The post {post} was not found in the database produced by populate_feed. ")
            self.assertEqual(post, p.title, f"The post {p.title} does not have the expected title: {post}.")
            self.assertEqual(exp_posts[post]["picture"], p.picture, f"The post {p.title} does not have the expected image.")
            self.assertEqual(exp_posts[post]["creator"], p.creator, f"The post {p.title} does not have the expected creator.")

    def test_post_objects_have_likes(self):
        posts = Post.objects.filter()
        for post in posts:
            self.assertTrue(post.likes>0, f"The post '{post.title}' has negative/zero likes.")

    def test_post_category(self):
        post1 = Categorises.objects.filter(post = 1)
        post2 = Categorises.objects.filter(post = 2)
        post3 = Categorises.objects.filter(post = 3)
        self.assertEqual(post1.category, "Craft",f"Post 1 has category '{post1.category}', expected 'Craft'.")
        self.assertEqual(post2.category, "Diy",f"Post 2 has category '{post2.category}', expected 'Diy'.")
        self.assertEqual(post3.category, "Cook",f"Post 3 has category '{post3.category}', expected 'Cook'.")


    def test_users(self):
        users = [UserProfile.objects.get(username = un) for un in ["bob", "dummy2"]]
        exp_users =[{"username":"bob", "email":"example@example.com", "first_name":"bob", "last_name":"the builder", "password":"password"}, 
        {"username":"dummy2", "email":"2@dummy.com", "first_name":"dum", "last_name":"my", "password":"dummy_password"}]
        for i in range(2):
            self.assertEqual(users[i].email, exp_users[i]["email"], f"{users[i].username}'s email is incorrect.")
            self.assertEqual(users[i].first_name, exp_users[i]["first_name"], f"{users[i].username}'s first name is incorrect.")
            self.assertEqual(users[i].last_name, exp_users[i]["last_name"], f"{users[i].username}'s last name is incorrect.")
            self.assertEqual(users[i].password, exp_users[i]["password"], f"{users[i].username}'s password is incorrect.")

    def test_user_follows(self):
        follow = FollowsUser.objects.get(follower = "bob")
        self.assertEqual(follow.following, "dummy2", f"Bob not following dummy2.")

    def test_user_likes(self):
        like = Likes.objects.filter(liker = "bob")
        self.assertEqual(1, len(like), f"Bob has liked {len(like)} posts - expected 1.")
        self.assertEqual(like[0].liked_post, 1, f"Expected liked post to have id 1, was {like[0].liked_post.id}")

    def test_attempts(self):
        pass

    def test_user_follows_category(self):
        follow = FollowsCategory.objects.get(follower = "bob")
        self.assertEqual(follow.following, "Diy", f"Bob not following diy.")

    def test_comments(self):
        comment = Comment.objects.get(id = 1)
        self.assertEqual(comment.post, 1, f"Expected commented post to have id 1, has {comment.post}.")
        self.assertEqual(comment.user, 1, f"Expected commenting user to have id 1, has id {comment.user}.")
        self.assertEqual(comment.comment, "That is dope!", f"Expected comment to be 'That is dope!', was {comment.comment}.")

    def test_folders(self):
        folder = Folder.objects.get(id = 1)
        self.assertEqual(folder.name, "Folder Name", f"Expected folder to have name 'Folder Name', has name {folder.name}.")
        self.assertEqual(folder.user, 1, f"Expected folder to have creator 1, has creator {folder.user}.")
        self.assertFalse(folder.private, f"Expected folder to be public.")

    def test_folders_post(self):
        folder_content = In_folder.objects.filter(folder = 1)
        self.assertEqual(len(folder_content), 1, f"Expected folder to contain 1 post, conttains {len(folder_content)}.")
        self.assertEqual(folder_content[0].post, 1, f"Expected folder to contain post 1, contains post {folder_content[0].post}.")
    

# admin interface tests
class AdminTests(TestCase):

    def setUp(self):
        User.objects.create_superuser('testAdmin', 'email@email.com', 'adminPassword123')
        self.client.login(username='testAdmin', password='adminPassword123')
        
        Helper.create_model_setup()

    def test_admin_interface_accessible(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200, f"The admin interface is not accessible. Check that you didn't delete the 'admin/' URL pattern in your project's urls.py module.")

    def test_models_present(self):
        response = self.client.get('/admin/')
        response_body = response.content.decode()

        self.assertTrue('Models in the Feed application' in response_body, f"The Feed app wasn't listed on the admin interface's homepage.")
        self.assertTrue('Categories' in response_body, "Category model not found in admin interface.")
        self.assertTrue('Posts' in response_body, "Post model not found in admin interface.")
        self.assertTrue('Comments' in response_body, "Comment model not found in admin interface.")
        self.assertTrue('Folders' in response_body, "Folder model not found in admin interface.")
        self.assertTrue('User profiles' in response_body, "UserProfile model not found in admin interface.")

    def test_post_display(self):
        response = self.client.get('/admin/feed/post/')
        response_body = response.content.decode()

        self.assertTrue('<div class="text"><a href="?o=1">Creator</a></div>' in response_body, f"The 'Creator' column could not be found in the admin interface for the Post model.")
        self.assertTrue('<div class="text"><a href="?o=2">Title</a></div>' in response_body, f"The 'Title' column could not be found in the admin interface for the Post model.")
        self.assertTrue('<div class="text"><a href="?o=3">Likes</a></div>' in response_body, f"The 'Likes' column could not be found in the admin interface for the Post model.")
        self.assertTrue('<div class="text"><span>Comments</span></div>' in response_body, f"The 'Comments' column could not be found in the admin interface for the Post model.")

        self.assertTrue('<td class="field-title">test attempt</td>' in response_body, "Could not find post 'test attempt' in admin interface.")    

    def test_userprofile_display(self):
        response = self.client.get('/admin/feed/userprofile/')
        response_body = response.content.decode()

        self.assertTrue('<div class="text"><a href="?o=1">User</a></div>' in response_body, f"The 'User' column could not be found in the admin interface for the Userprofile model.")
        self.assertTrue('<div class="text"><span>Email</span></div>' in response_body, f"The 'Email' column could not be found in the admin interface for the Userprofile model.")
        self.assertTrue('<div class="text"><span>Posts</span></div>' in response_body, f"The 'Posts' column could not be found in the admin interface for the Userprofile model.")
        self.assertTrue('<div class="text"><span>Follows</span></div>' in response_body, f"The 'Follows' column could not be found in the admin interface for the Userprofile model.")
        self.assertTrue('<div class="text"><span>Followers</span></div>' in response_body, f"The 'Followers' column could not be found in the admin interface for the Userprofile model.")

        self.assertTrue('<th class="field-user nowrap"><a href="/admin/feed/userprofile/1/change/">bobs</a></th>' in response_body, "Cound not find use bobs in admin interface.")
        self.assertTrue('<td class="field-followers">1</td>' in response_body, "Could not find bobs's number of followers (expected 1).")
    def test_category_display(self):
        response = self.client.get('/admin/feed/category/')
        response_body = response.content.decode()

        self.assertTrue('<div class="text"><span>Category</span></div>' in response_body, f"The 'Category' column could not be found in the admin interface for the Category model.")

    def test_comment_display(self):
        response = self.client.get('/admin/feed/comment/')
        response_body = response.content.decode()

        self.assertTrue('<div class="text"><a href="?o=1">Comment</a></div>' in response_body, f"The 'Comment' column could not be found in the admin interface for the Comment model.")
        self.assertTrue('<div class="text"><a href="?o=2">User</a></div>' in response_body, f"The 'User' column could not be found in the admin interface for the Comment model.")
        self.assertTrue('<div class="text"><a href="?o=3">Post</a></div>' in response_body, f"The 'Post' column could not be found in the admin interface for the Comment model.")
        self.assertTrue('<div class="text"><a href="?o=4">Likes</a></div>' in response_body, f"The 'Likes' column could not be found in the admin interface for the Comment model.")

        self.assertTrue('<th class="field-comment"><a href="/admin/feed/comment/1/change/">test comment</a></th>' in response_body, "Could not find 'test comment' in admin interface.")

    def test_folder_display(self):
        response = self.client.get('/admin/feed/folder/')
        response_body = response.content.decode()

        self.assertTrue('<div class="text"><a href="?o=1">Name</a></div>' in response_body, f"The 'Name' column could not be found in the admin interface for the Folder model.")
        self.assertTrue('<div class="text"><a href="?o=2">User</a></div>' in response_body, f"The 'User' column could not be found in the admin interface for the Folder model.")
        self.assertTrue('<div class="text"><span>Posts</span></div>' in response_body, f"The 'Posts' column could not be found in the admin interface for the Folder model.")
        self.assertTrue('<div class="text"><a href="?o=4">Private</a></div>' in response_body, f"The 'Private' column could not be found in the admin interface for the Folder model.")

        self.assertTrue('<th class="field-name"><a href="/admin/feed/folder/1/change/">test folder</a></th>' in response_body, "Could not find 'test folder' in admin interface for the Folder model.")


# helper functions, for helping
class Helper:
    def create_model_setup():
        diy = Category.objects.create(name="diy")
        diy.save()
        food = Category.objects.create(name = "food")
        food.save()

        user1 = User.objects.create(username = "bobs", email = "bob@gmail.com", password = "abc1234", first_name = "bob", last_name = "smith")
        user1.save()
        user1p = UserProfile.objects.create(user = user1, bio = "a bio")
        user1p.profile_picture.save("sample_1.jpg", ImageFile(open("sample_images/sample_1.jpg", "rb")))
        user2 = User.objects.create(username = "alicej", email = "alice@gmail.com", password = "testpassword", first_name = "alice", last_name = "jones")
        user2.save()
        user2p = UserProfile.objects.create(user = user2, bio = "a bio")
        user2p.profile_picture.save("sample_2.jpg", ImageFile(open("sample_images/sample_2.jpg", "rb")))
        

        post = Post.objects.create(id = 1, creator = user1p, title = "test", likes = 0)
        post.picture.save("sample_1.jpg", ImageFile(open("sample_images/sample_1.jpg", "rb")))

        attempt_post = Post.objects.create(id = 2, creator = user2p, title = "test attempt", likes =0)
        attempt_post.picture.save("sample_2.jpg", ImageFile(open("sample_images/sample_2.jpg", "rb")))
        attempt_post.original = 1
        attempt_post.save()
        

        comment1 = Comment.objects.create(post_id = 1, user_id =1, comment = "test comment", likes = 0)
        comment1.save()
        comment2 = Comment.objects.create(post_id = 1, user_id = 2, comment = "another test comment", likes = 0)
        comment2.save()

        Likes.objects.create(liker = user1p, liked_post = post)
        Likes.objects.create(liker = user2p, liked_post = post)
        Likes.objects.create(liker = user1p, liked_post = attempt_post)

        FollowsCategory.objects.create(follower = user1p, following = diy)
        FollowsCategory.objects.create(follower = user1p, following = food)
        FollowsCategory.objects.create(follower = user2p, following = diy)

        Categorises.objects.create(post = post, category = diy)
        Categorises.objects.create(post = attempt_post, category = diy)

        FollowsUser.objects.create(follower = user2p, following = user1p)

        folder = Folder.objects.create(id = 1, name = "test folder", user = user1p)
        folder.save()
        In_folder.objects.create(folder = folder, post = post)

    def get_template(path_to_template):
        f = open(path_to_template, 'r')
        template_str = ""

        for line in f:
            template_str = f"{template_str}{line}"

        f.close()
        return template_str