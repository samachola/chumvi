from app import app, user
import unittest
import flask_testing

User = user.User

class TestJikoni(unittest.TestCase):
    
    def setUp(self):
        self.user_list = []
        self.new_user = User('sam achola', 'sam.achola@live.com', '123')
        self.current_person = dict(email=self.new_user.email, categories=self.new_user.categories, recipes=self.new_user.recipes)
        self.user_list.append(self.new_user)


    def tearDown(self):
        pass
    
    def signup(self):
        """Signup helper method"""
        tester = app.test_client(self)
        return tester.post('/register', data=dict(name='Sam Achola', email='sam.achola@live.com', password='123'), follow_redirects=True)
        # self.new_user = User('sam achola', 'sam.achola@live.com', '123')
        # self.user_list.append(self.new_user)
        # return self.user_list

    def login(self):
        """Login helper method"""
        tester = app.test_client(self)
        return tester.post('/login', data=dict(email='sam.achola@live.com', password='123', follow_redirects=True)) 
    def add_category(self):
        """Add Category Helper Method"""
        tester = app.test_client(self)
        return tester.post('/category', data=dict(title="Breakfast", description="Breakfast is awesome"))

    def add_recipe(self):
        """Add recipe helper method"""
        tester = app.test_client(self)
        return tester.post('/addrecipe', data=dict(title='Githeri', category='Breakfast', ingredients='Maize, Beans', process='Just boil and add salt. Enjoy!'), follow_redirects=True)

    # Ensures that flask is correctly setup
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_registration_username(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(name='', email='sam.achola@live.com', password='123'))
        self.assertIn(b'Name cannot be an empty string', response.data, msg="User Without Name Failed")

    def test_registration_email(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(name='sam', email='not valid email', password='123'))
        self.assertIn(b'Email provided is not valid', response.data, msg="Check Valid Email Failed")


    def test_registration_params(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(name='Sam Achola', email='sam.achola@live.com', password='123'), follow_redirects=True)
        self.assertIn(b'Login', response.data, msg="Post registration Failed")

    def test_login_email(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(email='sam', password='123'))
        self.assertIn(b'Enter a valid email address', response.data, msg="Post Login Failed")

    def test_login_empty_fields(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(email='', password=''))
        self.assertIn(b'Email and Password Fields are Required', response.data, msg="Post Login Failed")

    def test_login_unexisting(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(email='sam.acho@live.com', password='123'), follow_redirects=True)
        self.assertIn(b'Username and Password incorrect', response.data, msg="Login Failed")

   
    def test_view_categories_unprotected(self):
        tester = app.test_client(self)
        response = tester.get('/category', follow_redirects=True)
        self.assertIn(b'Login', response.data, msg="Category route not protected")

    def test_edit_category_unprotected(self):
        tester = app.test_client(self)
        response = tester.get('/edit_category/0', follow_redirects=True)
        self.assertIn(b'Login', response.data, msg="Category route not protected")

    def test_view_recipe_unprotected(self):
        tester = app.test_client(self)
        response = tester.get('/recipes', follow_redirects=True)
        self.assertIn(b'Login', response.data, msg="Category route not protected")

    def test_edit_recipe_unprotected(self):
        tester = app.test_client(self)
        response = tester.get('/edit/0', follow_redirects=True)
        self.assertIn(b'Login', response.data, msg="Category route not protected")

    def test_login(self):
        tester = app.test_client(self)
        self.signup()
        response = tester.post('/login', data=dict(email='sam.achola@live.com', password='123'), follow_redirects=True)
        self.assertIn(b'Recipes', response.data, msg="Could not login")
        


    def test_add_recipe(self):
        tester = app.test_client(self)
        self.signup()
        self.login()
        self.add_category()
        response = tester.post('/addrecipe', data=dict(title='Githeri', category='Breakfast', ingredients='Maize, Beans', process='Just boil and add salt. Enjoy!'), follow_redirects=True)
        self.assertIn(b'Githeri', response.data, msg="recipe add function not working")
    
    def test_view_recipe(self):
        tester = app.test_client(self)
        self.signup()
        self.login()
        self.add_category()
        self.add_recipe()
        response = tester.get('/recipes', content_type='html/text')
        self.assertIn(b'Githeri', response.data, msg="No recipes found")

    def test_view_single_recipe(self):
        tester = app.test_client(self)
        self.signup()
        self.login()
        self.add_category()
        self.add_recipe()
        response = tester.get('/view/0', content_type='html/text')
        self.assertIn(b'Maize, Beans', response.data, msg='Could not view single recipe')

    def test_delete_recipe(self):
        tester = app.test_client(self)
        self.signup()
        self.login()
        self.add_category()
        self.add_recipe()
        response = tester.get('/delete/0', follow_redirects=True)
        self.assertIn(b'My Recipes', response.data, msg='could not delete recipe')

    def test_add_category(self):
        tester = app.test_client(self)
        self.signup()
        self.login()
        response = tester.post('/category', data=dict(title="Breakfast", description="Breakfast is awesome"), follow_redirects=True)
        self.assertIn(b'Breakfast', response.data, msg="Add Category Failed!")

    def test_view_category(self):
        tester = app.test_client(self)
        self.signup()
        self.login()
        self.add_category()
        response = tester.get('/edit_category/0', content_type='html/text')
        self.assertIn(b'Breakfast', response.data, msg='Could not view category')


    def test_update_category(self):
        tester = app.test_client(self)
        self.signup()
        self.login()
        self.add_category()
        response = tester.post('/edit_category/0', data=dict(title="Lunch", description="Breakfast is awesome"), follow_redirects=True)
        self.assertIn(b'Lunch', response.data, msg='Could not update category')

    def test_delete_category(self):
        tester = app.test_client(self)
        self.signup()
        self.login()
        self.add_category()
        response = tester.get('/category/0', content_type='html/text', follow_redirects=True)        
        self.assertIn(b'Breakfast', response.data, msg='Could not delete category')


if __name__ == '__main__':
    unittest.main()