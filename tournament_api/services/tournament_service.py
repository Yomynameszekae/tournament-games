from django.shortcuts import get_object_or_404
from ..models import Tournament, Stage

class TournamentService:

    @staticmethod
    def determine_winner(tournament_id):
        tournament = get_object_or_404(Tournament, pk=tournament_id)
        final_stage = Stage.objects.filter(tournament=tournament, stage_type='KNOCKOUT').first()
        if not final_stage:
            return None
        final_round = final_stage.rounds.order_by('-sequence').first()
        if not final_round:
            return None
        final_match = final_round.matches.first()
        if not final_match:
            return None
        
        if final_match.home_team_score > final_match.away_team_score:
            winner = final_match.home_team
        else:
            winner = final_match.away_team
        
        return winner
