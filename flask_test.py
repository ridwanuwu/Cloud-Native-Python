from app import app
import unittest

class FlaskappTests(unittest.TestCase):
 def setUp(self):
  # create a test client
  self.app = app.test_client()
  # propagate the exceptions to the test client
  self.app.testing = True

 def test_users_status_code(self):
  # sends HTTP GET request to the application
  result = self.app.get('/api/v1/users')
  # assert the status code of the response
  self.assertEqual(result.status_code, 200)

 def test_tweets_status_code(self):
  # sends HTTP GET request to the application
  result = self.app.get('/api/v2/tweets')
  # assert the status code of the response
  self.assertEqual(result.status_code, 200)

 def test_info_status_code(self):
  # sends HTTP GET request to the application
  result = self.app.get('/api/v1/info')
  # assert the status code of the response
  self.assertEqual(result.status_code, 200)

 def test_addusers_status_code(self):
  # sends HTTP POST request to the application
  result = self.app.post('/api/v1/users', data='{"username": "mahesh404", "email":"manishtest@gmail.com", "password": "test123"}', content_type='application/json')
  print (result)
  # assert the status code of the response
  self.assertEqual(result.status_code, 201)

 def test_updusers_status_code(self):
  # sends HTTP PUT request to the application
  # on the specified path
  result = self.app.put('/api/v1/users/2', data='{"password": "coba"}', content_type='application/json')
  # assert the status code of the response
  self.assertEqual(result.status_code, 200)

 def test_addtweets_status_code(self):
  # sends HTTP POST request to the application
  # on the specified path
  result = self.app.post('/api/v2/tweets', data='{"username": "mahesh@rocks", "body":"Wow! Is it working"}', content_type='application/json')
  # assert the status code of the response
  self.assertEqual(result.status_code, 200)

 def test_deluser_status_code(self):
  # sends HTTP DELETE request to the application
  result = self.app.delete('/api/v1/users', data='{"username": "lala"}', content_type='application/json')
  # assert the status code of the response
  self.assertEqual(result.status_code, 200)
