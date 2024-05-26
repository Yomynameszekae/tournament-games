from django.shortcuts import get_object_or_404
from .stage_service import StageService
from ..models import Round, Fixture, Match, Stage, Game
from django.utils import timezone

class RoundService:

    @staticmethod
    def generate_fixtures(stage_id, round_id=None):
        stage = get_object_or_404(Stage, pk=stage_id)
        fixtures = []

        if not stage.rounds.exists():
            # Create initial round and fixtures if no rounds exist
            initial_round = Round.objects.create(stage=stage, sequence=1, name="Initial Knockout Round", bracket_side=None)
            fixtures = RoundService.generate_initial_knockout_round(stage, initial_round)
        else:
            if round_id:
                # Generate fixtures for the next round
                current_round = get_object_or_404(Round, pk=round_id)
                next_round_sequence = current_round.sequence + 1
                next_rounds = Round.objects.filter(stage=stage, sequence=next_round_sequence)
                if not next_rounds.exists():
                    # Create next round if it doesn't exist
                    next_rounds = [
                        Round.objects.create(stage=stage, sequence=next_round_sequence, name=f"Knockout Round {next_round_sequence} (Left)", bracket_side='LEFT'),
                        Round.objects.create(stage=stage, sequence=next_round_sequence, name=f"Knockout Round {next_round_sequence} (Right)", bracket_side='RIGHT')
                    ]
                fixtures = RoundService.generate_next_knockout_round_fixtures(stage, current_round.sequence)
            else:
                raise ValueError("Round ID is required if the stage has existing rounds")

        return fixtures

    @staticmethod
    def generate_initial_knockout_round(stage, initial_round):
        qualifiers = StageService.determine_qualifiers(stage.id)
        
        if not qualifiers:
            raise ValueError("No qualifiers found for the knockout stage")

        game = stage.tournament.game
        max_teams = game.max_teams_per_match

        # Split qualifiers into left and right brackets if max_teams is 2
        if max_teams == 2:
            left_qualifiers = qualifiers[:len(qualifiers)//2]
            right_qualifiers = qualifiers[len(qualifiers)//2:]

            fixtures = []
            # Generate fixtures for left bracket
            while len(left_qualifiers) > 1:
                home_team = left_qualifiers.pop(0)
                away_team = left_qualifiers.pop(0)
                fixture = Fixture(round=initial_round, match_date=timezone.now())
                fixture.save()
                fixture.teams.add(home_team, away_team)
                fixtures.append(fixture)

            # Generate fixtures for right bracket
            while len(right_qualifiers) > 1:
                home_team = right_qualifiers.pop(0)
                away_team = right_qualifiers.pop(0)
                fixture = Fixture(round=initial_round, match_date=timezone.now())
                fixture.save()
                fixture.teams.add(home_team, away_team)
                fixtures.append(fixture)
        else:
            # Generate fixtures for multiple teams per match
            fixtures = []
            while len(qualifiers) >= max_teams:
                teams_for_fixture = [qualifiers.pop(0) for _ in range(max_teams)]
                fixture = Fixture(round=initial_round, match_date=timezone.now())
                fixture.save()
                fixture.teams.add(*teams_for_fixture)
                fixtures.append(fixture)

        Fixture.objects.bulk_create(fixtures)
        return fixtures

    @staticmethod
    def generate_next_knockout_round_fixtures(stage, current_round_sequence):
        current_rounds = Round.objects.filter(stage=stage, sequence=current_round_sequence)
        next_round_sequence = current_round_sequence + 1
        next_rounds = Round.objects.filter(stage=stage, sequence=next_round_sequence)
        
        fixtures = []

        for next_round in next_rounds:
            if next_round.bracket_side in ['LEFT', 'RIGHT']:
                previous_round = current_rounds.filter(bracket_side=next_round.bracket_side).first()
                if previous_round:
                    previous_fixtures = Fixture.objects.filter(round=previous_round)
                    winners = []
                    for fixture in previous_fixtures:
                        match = fixture.match
                        winning_teams = []
                        for team in fixture.teams.all():
                            if team == match.winning_team():
                                winning_teams.append(team)
                        winners.extend(winning_teams)
                    max_teams = stage.tournament.game.max_teams_per_match
                    while len(winners) >= max_teams:
                        teams_for_fixture = [winners.pop(0) for _ in range(max_teams)]
                        fixture = Fixture(round=next_round, match_date=timezone.now())
                        fixture.save()
                        fixture.teams.add(*teams_for_fixture)
                        fixtures.append(fixture)
            else:
                # This handles the final where winners from left and right meet
                left_round = current_rounds.filter(bracket_side='LEFT').first()
                right_round = current_rounds.filter(bracket_side='RIGHT').first()
                if left_round and right_round:
                    left_winners = []
                    right_winners = []
                    left_fixtures = Fixture.objects.filter(round=left_round)
                    right_fixtures = Fixture.objects.filter(round=right_round)
                    for fixture in left_fixtures:
                        match = fixture.match
                        for team in fixture.teams.all():
                            if team == match.winning_team():
                                left_winners.append(team)
                    for fixture in right_fixtures:
                        match = fixture.match
                        for team in fixture.teams.all():
                            if team == match.winning_team():
                                right_winners.append(team)
                    if left_winners and right_winners:
                        teams_for_fixture = left_winners + right_winners
                        fixture = Fixture(round=next_round, match_date=timezone.now())
                        fixture.save()
                        fixture.teams.add(*teams_for_fixture)
                        fixtures.append(fixture)

        Fixture.objects.bulk_create(fixtures)
        return fixtures
