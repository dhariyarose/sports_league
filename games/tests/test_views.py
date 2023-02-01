from django.test import TestCase, Client
from django.urls import reverse

from games.models import Game

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('games_list')
        
    def test_game_list_GET(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 302)



