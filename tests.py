from app import app, user
import unittest
import flask_testing

User = user.User

class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        self.new_user = User('sam achola', 'sam.achola@live.com', '123')
        self.current_person = dict(email=self.new_user.email, categories=self.new_user.categories, recipes=self.new_user.recipes)
        self.user_list = []


    def tearDown(self):
        pass
    
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
        response = tester.post('/login', data=dict(email='sam@live.com', password='123'), follow_redirects=True)
        self.assertIn(b'User not available! Please register', response.data, msg="Login Failed")

    # def test_login(self):
    #     tester = app.test_client(self)
    #     self.new_user = User('Sam Achola', 'sam.achola@live.com', '123')
    #     self.user_list.append(self.new_user)
    #     response = tester.post('/login', data=dict(email='sam.achola@live.com', password='123'), follow_redirects=True)
    #     self.assertIn(b'Add Recipe', response.data, msg="Could not login")
        


    # def test_add_recipe(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/addrecipe', data=dict(title='Githeri', category='breakfast', ingredients='Maize, Beans', process='Just boil and add salt. Enjoy!'), follow_redirects=True)
    #     self.assertIn(b'My recipes', response.data, msg="recipe add function not working")

    # def test_add_category(self):
    #     self.test_registration_params()
    #     self.test_login()
    #     tester = app.test_client(self)
    #     response = tester.post('/category', data=dict(title="Breakfast", description="Breakfast is awesome"))
    #     self.assertIn(b'Breakfast', response.data, msg="Add Category Failed!")


if __name__ == '__main__':
    unittest.main()