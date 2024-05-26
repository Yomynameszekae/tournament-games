from django.db import models
from .stage import Stage

class Round(models.Model):
    name = models.CharField(max_length=255)
    stage = models.ForeignKey(Stage, related_name='rounds', on_delete=models.CASCADE)
    sequence = models.IntegerField(help_text="Order of the round in the stage")
    bracket_side = models.CharField(max_length=10, choices=[('LEFT', 'Left'), ('RIGHT', 'Right')], null=True, blank=True, help_text="Bracket side for elimination rounds")

    def __str__(self):
        return f"{self.name} ({self.stage})"
