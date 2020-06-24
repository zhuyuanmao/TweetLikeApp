from django.test import TestCase

# Create your tests here.
from .models import Profile
from tweetLike.apps.authentication.models import Author
from .views import ProfileRetrieveAPIView
from rest_framework.test import (
    APIRequestFactory,
    APIClient,
    APITestCase,
)
from django.contrib.auth import get_user_model
"""
Model Test
"""
class ProfileModelTest(TestCase):
    def create_author(self,email='test@user.com',username='testUser',password='secret'):
        return Author.objects.create_user(email,username,password)

    def setUp(self):
        author = self.create_author()
        Profile.objects.create(author=author,lastName='lastName', firstName ='firstName')

    def test_create_get_user_profile(self):
        profile = Profile.objects.get(author__username='testUser')
        self.assertTrue(isinstance(profile.author,Author))
        self.assertEqual(profile.get_display_name(),"firstName lastName")

"""
API Tests
"""
class ProfileAPITest(APITestCase):
    url = '/profiles/'
    def create_author(self,email='test@user.com',username='testUser',password='secret'):
        return Author.objects.create_user(email,username,password)

    def setUp(self):
        self.author = self.create_author()
        self.profile = Profile.objects.create(author=self.author,lastName='lastName', firstName ='firstName')
        self.client = APIClient()

    def test_retrieve_profile(self):
        testUrl = self.url+ self.author.username+'/'
        response = self.client.get(testUrl)
        self.assertEqual(response.status_code,200)
    def test_retrieve_does_not_exist_profile(self):
        testUrl = self.url +'doestnotexistuser'+'/'
        response = self.client.get(testUrl)
        self.assertEqual(response.status_code,404)