from django.test import TestCase
from tweetLike.apps.authentication.models import Author

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
