from django.test import TestCase
from django.contrib.auth.models import User

class TestModel(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(username='test_username',\
            email='test_user@gmail.com')
        user.set_password('password@123')
        user.save()

        self.assertEqual(str(user.email),'test_user@gmail.com')