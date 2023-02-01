from django.test import TestCase
from django.contrib.auth.models import User
from games.models import Game

class TestModel(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(username='test_username',\
            email='test_user@gmail.com')
        user.set_password('password@123')
        user.save()

        game = Game(name="Game1",description="Game 1: Description", no_of_teams=2, no_of_participants=2, created_by=user, updated_by=user)
        game.save()

        self.assertEqual(str(game),'Game1')


