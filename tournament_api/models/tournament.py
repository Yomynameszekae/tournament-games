from django.db import models
from .game import Game

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    game = models.ForeignKey(Game, related_name='tournaments', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
