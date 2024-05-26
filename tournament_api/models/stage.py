from django.db import models
from .tournament import Tournament

class Stage(models.Model):
    STAGE_TYPE_CHOICES = [
        ('LEAGUE', 'League'),
        ('KNOCKOUT', 'Knockout')
    ]
    
    name = models.CharField(max_length=255)
    stage_type = models.CharField(max_length=8, choices=STAGE_TYPE_CHOICES)
    tournament = models.ForeignKey(Tournament, related_name='stages', on_delete=models.CASCADE)
    number_of_qualifiers = models.IntegerField(help_text="Number of teams that qualify to the next stage (only applicable for league stages)")

    def __str__(self):
        return f"{self.name} ({self.get_stage_type_display()})"
