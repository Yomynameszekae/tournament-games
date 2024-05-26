from django.shortcuts import get_object_or_404
from ..models import Match

class FixtureService:

    @staticmethod
    def update_match_result(match_id, home_team_score, away_team_score):
        match = get_object_or_404(Match, pk=match_id)
        match.home_team_score = home_team_score
        match.away_team_score = away_team_score
        match.save()
        return match
