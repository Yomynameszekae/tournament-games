from django.db import models
from django.utils import timezone
from .round import Round
from .team import Team

class Fixture(models.Model):
    round = models.ForeignKey(Round, related_name='fixtures', on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team, related_name='fixtures')
    match_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" vs ".join([team.name for team in self.teams.all()]) + f" ({self.round})"
