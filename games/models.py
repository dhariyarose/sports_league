from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from .unique_slugify import unique_slugify
from django.utils.translation import gettext_lazy as _
# Create your models here.
  
# declare a new model with a name "Game"
class Game(models.Model):
 
    # fields of the model
    name = models.CharField(max_length = 200)
    description = models.TextField()
    no_of_teams = models.IntegerField(null=True,blank=True)
    no_of_participants = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,null=True,blank=True,on_delete=models.PROTECT,related_name="created_by")
    updated_by = models.ForeignKey(User,null=True,blank=True,on_delete=models.PROTECT,related_name="updated_by")
    slug = models.SlugField(null=True, blank=True,unique=True,help_text=_("The name of the page as it will appear in URLs"))

    def save(self, *args, **kwargs):
        unique_slugify(self,self.name)
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )