from django.db import models

# Create your models here.
class Player(models.Model):
    player_name = models.CharField(max_length=50)