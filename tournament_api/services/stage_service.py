from django.shortcuts import get_object_or_404
from ..models import Stage, Match

class StageService:

    @staticmethod
    def determine_qualifiers(stage_id):
        stage = get_object_or_404(Stage, pk=stage_id)
        if stage.stage_type != 'KNOCKOUT':
            return []
        
        previous_stage = Stage.objects.filter(tournament=stage.tournament, stage_type='LEAGUE').first()
        if not previous_stage:
            return []
        
        previous_rounds = previous_stage.rounds.all()
        matches = Match.objects.filter(fixture__round__in=previous_rounds, game_stats__isnull=False)
        
        game = stage.tournament.game
        team_points = {team.id: 0 for team in stage.tournament.teams.all()}
        
        if game.name == 'Fortnite':
            for match in matches:
                for team in match.fixture.teams.all():
                    team_stats = match.game_stats.get(str(team.id), {})
                    team_points[team.id] += team_stats.get('damage_done', 0)
        elif game.name == 'Call of Duty':
            for match in matches:
                for team in match.fixture.teams.all():
                    team_stats = match.game_stats.get(str(team.id), {})
                    team_points[team.id] += team_stats.get('kills', 0)
        elif game.name == 'Apex':
            for match in matches:
                for team in match.fixture.teams.all():
                    team_stats = match.game_stats.get(str(team.id), {})
                    team_points[team.id] += team_stats.get('kills', 0)
        elif game.name == 'Tekken':
            for match in matches:
                for team in match.fixture.teams.all():
                    team_stats = match.game_stats.get(str(team.id), {})
                    team_points[team.id] += team_stats.get('score', 0)
        elif game.name == 'Fifa':
            for match in matches:
                for team in match.fixture.teams.all():
                    team_stats = match.game_stats.get(str(team.id), {})
                    team_points[team.id] += team_stats.get('Goals', 0)
        else:
            raise ValueError(f"Unsupported game type: {game.name}")

        sorted_teams = sorted(stage.tournament.teams.all(), key=lambda team: team_points[team.id], reverse=True)
        qualifiers = sorted_teams[:stage.number_of_qualifiers]
        return qualifiers
