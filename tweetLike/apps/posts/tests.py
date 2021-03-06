from django.test import TestCase

# Create your tests here.
from .models import Post,Comment
from tweetLike.apps.authentication.models import Author

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
class PostModelTest(TestCase):
    def create_author(self,email='test@user.com',username='test',password='secret'):
        return Author.objects.create_user(email,username,password)
    def setUp(self):
        self.author = self.create_author()
        self.post = Post.objects.create(
            title='Test Title',
            description='This is test description',
            content='This is test content',
            author = self.author.profile,
            )

    def test_create_post_model(self):
        self.assertTrue(isinstance(self.post,Post))
        self.assertTrue(self.post.slug != None)

"""
API Tests
"""
class PostAPITest(APITestCase):
    url = '/posts'
    post_data = {
        "post":{
            "title":"How to train your dragon",
            "description":"Ever wonder how?",
            "content":"You have to believe",
        }
    }
    profile_data = {
        "user": {
            "bio":"Hello World",
            "firstName":"John",
            "lastName": "Doe",
            "github":"https://github.com/test/"
        }
    }
    def create_author(self,email='test@user.com',username='test',password='secret'):
        return Author.objects.create_user(email,username,password)
    
    def setUp(self):
        self.author = self.create_author()
        self.client = APIClient()
        self.client.force_authenticate(user=self.author)
        self.client.put('/user/',data=self.profile_data,format='json')
        self.post = Post.objects.create(
            title="How to train your dragon",
            description="Ever wonder how?",
            content="You have to believe",
            author = self.author.profile,
        )

    def test_retrieve_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)

    def test_create_post(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.post(self.url,data=self.post_data,format='json')
        self.assertEqual(response.status_code,201)
    
    def test_retrieve_single_post(self):
        response = self.client.get(self.url+'/'+self.post.slug)
        self.assertEqual(response.status_code,200)
    
    def test_retrieve_does_not_exist_post(self):
        response = self.client.get(self.url+'/'+'does-not-exist')
        self.assertEqual(response.status_code,404)

    def test_update_single_post(self):
        mask_data = {
            "post":{
                "title":"How to train your dragon 2",
                "description":"Ever wonder how?",
                "content":"You have to believe",
            }
        }
        self.client.force_authenticate(user=self.author)
        response = self.client.put(self.url+'/'+self.post.slug, data=mask_data,format='json')
        self.assertEqual(response.status_code,200)

class CommentAPITest(APITestCase):
    url = '/posts'
    post_data = {
        "post":{
            "title":"How to train your dragon",
            "description":"Ever wonder how?",
            "content":"You have to believe",
        }
    }
    profile_data = {
        "user": {
            "bio":"Hello World",
            "firstName":"John",
            "lastName": "Doe",
            "github":"https://github.com/test/"
        }
    }
    def create_author(self,email='test@user.com',username='test',password='secret'):
        return Author.objects.create_user(email,username,password)
    
    def setUp(self):
        self.author = self.create_author()
        self.client = APIClient()
        self.client.force_authenticate(user=self.author)
        self.client.put('/user/',data=self.profile_data,format='json')
        self.post = Post.objects.create(
            title="How to train your dragon",
            description="Ever wonder how?",
            content="You have to believe",
            author = self.author.profile,
        )
        self.comment = Comment.objects.create(
            body = 'It takes a Jacobian',
            post = self.post,
            author = self.author.profile
        )
    def test_get_comments(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.get(self.url+'/'+self.post.slug+'/comments/')
        self.assertEqual(response.status_code,200)

    def test_get_single_comment(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.get(self.url+'/'+self.post.slug+'/comments/'+str(self.comment.id)+'/')
        self.assertEqual(response.status_code,200)

    def test_delete_single_comment(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.delete(self.url+'/'+self.post.slug+'/comments/'+str(self.comment.id)+'/')
        self.assertEqual(response.status_code,204)





        
        
