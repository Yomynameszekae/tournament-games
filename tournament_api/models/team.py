from django.db import models
from .tournament import Tournament

class Team(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)
    tournament = models.ForeignKey(Tournament, related_name='teams', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
