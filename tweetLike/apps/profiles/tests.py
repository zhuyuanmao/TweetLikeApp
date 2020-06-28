from django.test import TestCase

# Create your tests here.
from .models import Profile
from tweetLike.apps.authentication.models import Author
from .views import ProfileRetrieveAPIView
from rest_framework.test import (
    APIRequestFactory,
    APIClient,
    APITestCase,
    force_authenticate
)

from django.contrib.auth import get_user_model
"""
Model Test
"""
class ProfileModelTest(TestCase):
    def create_author(self,email='test@user.com',username='testUser',password='secret'):
        return Author.objects.create_user(email,username,password)

    def setUp(self):
        self.author = self.create_author()
        
    def test_create_get_user_profile(self):
        self.assertTrue(isinstance(self.author.profile,Profile))
        self.assertTrue(isinstance(self.author.profile.author,Author))
        self.assertEqual(self.author.profile.get_display_name()," ")

"""
API Tests
"""
class ProfileAPITest(APITestCase):
    url = '/profiles/'
    profile_data = {
        "user": {
            "bio":"Hello World",
            "firstName":"John",
            "lastName": "Doe",
            "github":"https://github.com/test/"
        }
    }
    def create_author(self,email='test@user.com',username='testUser',password='secret'):
        return Author.objects.create_user(email,username,password)

    def setUp(self):
        self.author = self.create_author()
        self.client = APIClient()

    def test_retrieve_profile(self):
        testUrl = self.url+ self.author.username
        response = self.client.get(testUrl)
        self.assertEqual(response.status_code,200)

    def test_retrieve_does_not_exist_profile(self):
        testUrl = self.url +'doestnotexistuser'
        response = self.client.get(testUrl)
        self.assertEqual(response.status_code,404)
    
    def test_update_user_profile(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.put('/user/',data=self.profile_data,format='json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(self.author.profile.bio,self.profile_data['user'].get('bio'))
        self.assertEqual(self.author.profile.firstName,self.profile_data['user'].get('firstName'))
        self.assertEqual(self.author.profile.lastName,self.profile_data['user'].get('lastName'))
        self.assertEqual(self.author.profile.github,self.profile_data['user'].get('github'))
        self.assertEqual(self.author.profile.get_display_name(),"John Doe")

class ProfileFollowAPITest(APITestCase):
    url = '/profiles/'
    profile_data = {
        "user": {
            "bio":"Hello World",
            "firstName":"John",
            "lastName": "Doe",
            "github":"https://github.com/test/"
        }
    }
    def create_author(self,email='test@user.com',username='testUser',password='secret'):
        return Author.objects.create_user(email,username,password)

    def setUp(self):
        self.author = self.create_author()
        self.follow1 = self.create_author(email='test1@user.com',username='testUser1',password='secret')
        self.follow2 = self.create_author(email='test2@user.com',username='testUser2',password='secret')
        self.client = APIClient()
        self.author.profile.follow(self.follow1.profile)
       
    def test_following_myself(self):
        self.client.force_authenticate(user=self.author)
        url = '/profiles/'+self.author.username+'/follow'
        respone = self.client.post(url)
        self.assertEqual(respone.status_code,400)
    def test_unfollow_author(self):
        self.client.force_authenticate(user=self.author)
        url = '/profiles/'+self.follow1.username+'/follow'
        response = self.client.delete(url)
        self.assertEqual(response.status_code,204)
    def test_follow_author(self):
        self.client.force_authenticate(user=self.author)
        url = '/profiles/'+self.follow1.username+'/follow'
        response = self.client.post(url)
        self.assertEqual(response.status_code,201)

        
        
        

        
