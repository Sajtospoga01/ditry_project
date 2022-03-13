import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

from feed.models import Category, Folder,Post, Queries,UserProfile,Categorises,Functions,FollowsUser,Comment
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

# all database related tests, getting there

class DatabaseConfigurationTests(TestCase):
    def test_databases_variable_exists(self):
        self.assertTrue(settings.DATABASES, f"Settings module doesn't have a DATABASE variable.")
        self.assertTrue('default' in settings.DATABASES, f"No default database configuration.")


class ModelTests(TestCase):
    def setup(self):
        for name in ["diy", "food"]:
            c = Category.objects.get_or_create(name=name)
            c.save()

        user = UserProfile.objects.create_user("alicej", "alice@gmail.com", "password")
        user.first_name = "alice"
        user.last_name = "jones"
        user.save()

        post = Post.objects.create(id = 1, creator = user, title = "test", likes = 3)
        post.picture.save("sample_1.jpg", ImageFile(open("sample_images/sample_1.jpg", "rb")))

        comment = Comment.objects.create(post_id = 1, user_id =1, comment = "test comment", likes = 0)

    def test_category_model(self):
        c_diy = Category.objects.get(name = "diy")
        self.assertTrue(c_diy.id>=0, f"Category id not autofilled.")
        c_food = Category.objects.get(name = "food")
        self.assertTrue(c_food.id > c_diy.id, f"Category id doesn't increment.")

    def test_post_model(self):
        post = Post.objects.get(id = 1)
        self.assertEqual(post.title, "test", f"Expected title test, got {post.title}.")
        self.assertEqual(post.creator, User.objects.get(username = "alicej"), f"Unexpected creator.")

    def test_str_methods(self):
        category_diy = Category.objects.get(name='diy')
        user_alice = User.objects.get(username = "alicej")
        test_post = Post.objects.get(id=1)
        test_comment = Comment.objects.get(id = 1)

        assertEqual(str(category_diy), "diy", f"Category string method doesn't work. Expected 'diy' and got '{str(category_diy)}'.")
        assertEqual(str(user_alice), "alicej1", f"UserProfile string method doesn't work. Expected 'alicej1' and got '{str(user_alice)}'.")
        assertEqual(str(test_post), "test", f"Post string method doesn't work. Expected 'test' and got '{str(test_post)}'.")
        assertEqual(str(test_comment), "test comment", f"Comment string method doesn't work. Expected 'test comment' and got '{str(test_comment)}'.")

    def test_likes_are_positive(self):
        p = Post.objects.create(creator = User.objects.get(username = "alicej"),title = "likes_test",likes = -1)
        p.picture.save("sample_2.jpg", ImageFile(open("sample_images/sample_2.jpg","rb")))
        self.assertTrue((p.likes >= 0), f"Post likes should not be negative.")
    
class UniqueConstraintTests(TestCase):
    def setup(self):
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
    def test_folder_unique(self);
        pass

class QueryTests(TestCase):
    def setup(self):
        pass
    def test_get_posts_in_category(self):
        pass
    def test_get_user_posts(self):
        pass
    def test_get_user_follows(self):
        pass

# tests for the population script, done except one
class PopulationScriptTests(TestCase):
    def setup(self):
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
        follow = FollowUser.objects.get(follower = "bob")
        self.assertEqual(follow.following, "dummy2", f"Bob not following dummy2.")

    def test_user_likes(self):
        like = Likes.objects.filter(liker = "bob")
        self.assertEqual(1, len(like), f"Bob has liked {len(like)} posts - expected 1.")
        self.assertEqual(like[0].liked_post, 1, f"Expected liked post to have id 1, was {like[0].liked_post.id}")

    def test_attemps(self):
        ## unimplemented

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
        folder_content = In_Folder.objects.filter(folder = 1)
        self.assertEqual(len(folder_content), 1, f"Expected folder to contain 1 post, conttains {len(folder_content)}.")
        self.assertEqual(folder_content[0].post, 1, f"Expected folder to contain post 1, contains post {folder_content[0].post}.")
    

# admin interface tests
# chap 5 has some
class AdminTests(TestCase):
    pass

# helper functions, for helping
class Helper:
    def create_user_object():
    user = User.objects.get_or_create(username='bobs',
                                      first_name='bob',
                                      last_name='smith',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user

def create_super_user_object():
    return User.objects.create_superuser('admin', 'admin@test.com', 'testpassword')

def get_template(path_to_template):
    f = open(path_to_template, 'r')
    template_str = ""

    for line in f:
        template_str = f"{template_str}{line}"

    f.close()
    return template_str
