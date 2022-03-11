import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

from feed.models import Post

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

        self.assertTrue(index_mapping_exists, f"The home url mapping could not be found.")
        self.assertEqual(reverse('feed:home'), '/home/', f"home url lookup failed.")

    def test_home_view_with_no_posts(self):
        response = self.client.get(reverse('feed:home'))

        self.assertEqual(response.status_code, 200, f"Home page not returned with status code 200.")
        self.assertContains(reponse, 'Feed empty.', f"'Feed empty.' message not displayed.") ## not implemented
        self.assertQuerysetEqual(response.context['posts'], [], f" Non-empty posts context.") ## also not checked

    def test_home_view_with_posts(self):
        HelperMethods.add_post()
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
        self.assertTrue('craft' in categories_strs, f"The category 'craft' was expected but not created by populate_feed.")
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

    def test_users(self):
    
    def test_post_objects_have_likes(self): ## oh this will fail
        posts = Post.objects.filter()
        for post in posts:
            self.assertTrue(post.likes>0, f"The post '{post.title}' has negative/zero likes.")
    # def test_slug_line_creation(self): # probably not necessary
    #     category = Category(name='Random Category String')
    #     category.save()
    #     self.assertEqual(category.slug, 'random-category-string')

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
