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

if __name__ == '__main__':
    unittest.main()