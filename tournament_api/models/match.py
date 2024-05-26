from django.db import models
from django.utils import timezone
from .fixture import Fixture

class Match(models.Model):
    fixture = models.OneToOneField(Fixture, related_name='match', on_delete=models.CASCADE)
    match_date = models.DateTimeField(default=timezone.now)
    game_stats = models.JSONField(default=dict)  # Store game-specific stats as JSON

    def __str__(self):
        return f"{self.fixture} ({self.fixture.round})"

    def is_finished(self):
        # Determine if the match is finished based on the presence of scores for all teams
        game = self.fixture.round.stage.tournament.game
        if game.name in ['Fortnite', 'Call of Duty', 'Apex', 'Tekken', 'Fifa']:
            return all(str(team.id) in self.game_stats for team in self.fixture.teams.all())
        return False

    def winning_team(self):
        game = self.fixture.round.stage.tournament.game
        if game.name == 'Fortnite':
            return self.determine_winning_team_fortnite()
        elif game.name == 'Call of Duty':
            return self.determine_winning_team_cod()
        elif game.name == 'Apex':
            return self.determine_winning_team_apex()
        elif game.name == 'Tekken':
            return self.determine_winning_team_tekken()
        elif game.name == 'Fifa':
            return self.determine_winning_team_fifa()
        return None

    def determine_winning_team_fortnite(self):
        teams = self.fixture.teams.all()
        teams_stats = {team: self.game_stats.get(str(team.id), {}) for team in teams}
        ranked_teams = sorted(teams, key=lambda team: teams_stats[team].get('damage_done', 0), reverse=True)
        return ranked_teams[0] if ranked_teams else None

    def determine_winning_team_cod(self):
        teams = self.fixture.teams.all()
        teams_stats = {team: self.game_stats.get(str(team.id), {}) for team in teams}
        ranked_teams = sorted(teams, key=lambda team: teams_stats[team].get('kills', 0), reverse=True)
        return ranked_teams[0] if ranked_teams else None

    def determine_winning_team_apex(self):
        teams = self.fixture.teams.all()
        teams_stats = {team: self.game_stats.get(str(team.id), {}) for team in teams}
        ranked_teams = sorted(teams, key=lambda team: teams_stats[team].get('kills', 0), reverse=True)
        return ranked_teams[0] if ranked_teams else None

    def determine_winning_team_tekken(self):
        teams = self.fixture.teams.all()
        teams_stats = {team: self.game_stats.get(str(team.id), {}) for team in teams}
        ranked_teams = sorted(teams, key=lambda team: teams_stats[team].get('score', 0), reverse=True)
        return ranked_teams[0] if ranked_teams else None

    def determine_winning_team_fifa(self):
        teams = self.fixture.teams.all()
        teams_stats = {team: self.game_stats.get(str(team.id), {}) for team in teams}
        ranked_teams = sorted(teams, key=lambda team: teams_stats[team].get('Goals', 0), reverse=True)
        return ranked_teams[0] if ranked_teams else None
