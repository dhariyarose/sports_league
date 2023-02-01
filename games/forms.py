from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'


class GameUpdateForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('id','name','description','no_of_teams','no_of_participants')