from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
    
    # Ensures that flask is correctly setup
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login', data=dict(username='admin', password='password'), follow_redirects=True)
        self.assertIn(b'chumvi', response.data)

    def test_registration(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(fname='', lname='', username='', password=''))
        self.assertIn(b'All input fields are required', response.data, msg="Post registration Failed")



    def test_add_recipe_empty(self):
        tester = app.test_client(self)
        response = tester.post('/addrecipe', data=dict(title='', ingredients='', process=''))
        self.assertIn(b'cannot add empty recipe', response.data, msg="Recipe field should not be null")


    def test_add_recipe(self):
        tester = app.test_client(self)
        response = tester.post('/addrecipe', data=dict(title='Githeri', ingredients='Maize, Beans', process='Just boil and add salt. Enjoy!'), follow_redirects=True)
        self.assertIn(b'chumvi', response.data, msg="recipe add function not working")

if __name__ == '__main__':
    unittest.main()