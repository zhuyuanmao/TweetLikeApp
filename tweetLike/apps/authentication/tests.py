from django.test import TestCase
from tweetLike.apps.authentication.models import Author
from rest_framework.test import APIRequestFactory,APIClient,APITestCase,URLPatternsTestCase

"""
Model Tests
"""
class AuthorModelTest(TestCase):
    def create_author(self,email ="John_Doe@test.com",username="johndoe",password="test"):
        return Author.objects.create_user(email,username,password)

    def test_author_creation(self):
        author = self.create_author()
        self.assertTrue(isinstance(author,Author))
        self.assertEqual(str(author),author.email)
        self.assertEqual(author.get_username(),author.username)
"""
API Tests
"""
class AuthenticationAPITest(APITestCase):
    login_data = {
        "user": {
            "username":"yuanmao",
            "email": "yuanmao@user.com",
            "password":"1997zhu."
        }
    }
    def test_author_registration(self):
        """
        Makes registration by giving user info.
        """
        response = self.client.post('/users/',self.login_data,format='json')
        self.assertEqual(response.status_code,201)
    def test_author_registration_repeated_account_info(self):
        """
        Registrates user info twice.
        """
        response = self.client.post('/users/',self.login_data,format='json')
        self.assertEqual(response.status_code,201)
        response =  self.client.post('/users/',self.login_data,format='json')
        self.assertEqual(response.status_code,400)
        response.render()
        self.assertEqual(response.content.decode('UTF-8'),'{"errors":{"email":["author with this email already exists."],"username":["author with this username already exists."]}}')
    def test_author_login(self):
        """
        Login with correct user/password pair
        """
        response = self.client.post('/users/',self.login_data,format='json')
        self.assertEqual(response.status_code,201)
        response = self.client.post('/users/login/',self.login_data,format='json')
        self.assertEqual(response.status_code,200)
    def test_author_login_with_doesnonexist_user_info(self):
        """
        Login with does not exist user/password pair
        """
        response = self.client.post('/users/login/',self.login_data,format='json')
        self.assertEqual(response.status_code,400)
    def test_author_login_with_wrong_user_password(self):
        """
        Login with wrong user/password pair
        """
        response = self.client.post('/users/',self.login_data,format='json')
        self.assertEqual(response.status_code,201)

        mask_data =  {
            "user": {
                "username":"yuanmao",
                "email": "yuanmao@user.com",
                "password":"wrong"
            }
        }
        response = self.client.post('/users/login/',mask_data,format='json')
        self.assertEqual(response.status_code,400)


