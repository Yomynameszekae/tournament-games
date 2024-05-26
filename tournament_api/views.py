from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Tournament, Round, Stage
from .services import TournamentService, StageService, RoundService, FixtureService

# List of all tournaments
def tournament_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournament_list.html', {'tournaments': tournaments})

# Details of a specific tournament
def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    return render(request, 'tournament_detail.html', {'tournament': tournament})

def generate_fixtures(request, stage_id, round_id=None):
    try:
        fixtures = RoundService.generate_fixtures(stage_id, round_id)
        return JsonResponse({'status': 'success', 'fixtures': [str(fixture) for fixture in fixtures]})
    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

# Update match results
def update_match_result(request, match_id):
    home_team_score = request.POST.get('home_team_score')
    away_team_score = request.POST.get('away_team_score')
    match = FixtureService.update_match_result(match_id, home_team_score, away_team_score)
    return JsonResponse({'status': 'success', 'match': str(match)})

# Determine next round qualifiers
def determine_qualifiers(request, stage_id):
    qualifiers = StageService.determine_qualifiers(stage_id)
    return JsonResponse({'status': 'success', 'qualifiers': [team.name for team in qualifiers]})

# Determine the winner of the tournament
def determine_winner(request, tournament_id):
    winner = TournamentService.determine_winner(tournament_id)
    if winner:
        return JsonResponse({'status': 'success', 'winner': winner.name})
    return JsonResponse({'status': 'error', 'message': 'Winner not determined'})

def generate_initial_knockout_round(request, stage_id):
    try:
        fixtures = RoundService.generate_initial_knockout_round(stage_id)
        return JsonResponse({'status': 'success', 'fixtures': [str(fixture) for fixture in fixtures]})
    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def generate_next_knockout_round(request, stage_id, current_round_sequence):
    try:
        fixtures = RoundService.generate_next_knockout_round_fixtures(stage_id, current_round_sequence)
        return JsonResponse({'status': 'success', 'fixtures': [str(fixture) for fixture in fixtures]})
    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)})