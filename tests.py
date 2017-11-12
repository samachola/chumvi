from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
    
    # Ensures that flask is correctly setup
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(name='', email='', password=''))
        self.assertIn(b'All input fields are required', response.data, msg="Post registration Failed")


    def test_registration_params(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(name='Achola', email='hello@achola.io', password='123456'), follow_redirects=True)
        self.assertIn(b'Login', response.data, msg="Post registration Failed")

    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login', data=dict(username='admin', password='password'), follow_redirects=True)
        self.assertIn(b'chumvi', response.data)


    def test_add_recipe_empty(self):
        tester = app.test_client(self)
        response = tester.post('/addrecipe', data=dict(title='', category='', ingredients='', process=''))
        self.assertIn(b'cannot add empty recipe, all fields are requied', response.data, msg="Recipe field should not be null")


    def test_add_recipe(self):
        tester = app.test_client(self)
        response = tester.post('/addrecipe', data=dict(title='Githeri', category='breakfast', ingredients='Maize, Beans', process='Just boil and add salt. Enjoy!'), follow_redirects=True)
        self.assertIn(b'chumvi', response.data, msg="recipe add function not working")

if __name__ == '__main__':
    unittest.main()