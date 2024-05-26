from django.urls import path
from . import views

urlpatterns = [
    path('tournaments/', views.tournament_list, name='tournament_list'),
    path('tournament/<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
    path('round/<int:round_id>/generate_fixtures/', views.generate_fixtures, name='generate_fixtures'),
    path('match/<int:match_id>/update_result/', views.update_match_result, name='update_match_result'),
    path('stage/<int:stage_id>/qualifiers/', views.determine_qualifiers, name='determine_qualifiers'),
    path('tournament/<int:tournament_id>/winner/', views.determine_winner, name='determine_winner'),
    path('stage/<int:stage_id>/generate_initial_knockout/', views.generate_initial_knockout_round, name='generate_initial_knockout_round'),
    path('stage/<int:stage_id>/generate_next_knockout_round/<int:current_round_sequence>/', views.generate_next_knockout_round, name='generate_next_knockout_round'),
    path('stage/<int:stage_id>/generate_fixtures/', views.generate_fixtures, name='generate_fixtures'),
    path('stage/<int:stage_id>/generate_fixtures/<int:round_id>/', views.generate_fixtures, name='generate_fixtures_for_round'),
    
]
