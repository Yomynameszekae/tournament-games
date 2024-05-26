from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    max_teams_per_match = models.IntegerField(default=2)  # Default is 2 teams per match

    def __str__(self):
        return self.name
