from django.urls import path
from . import views


urlpatterns = [
    
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('games-list/', views.GamesList.as_view(), name='games_list'),
    path('game/new/', views.GameNew.as_view(), name='game_new'),
    path('game/delete/', views.GameDelete.as_view(), name='game_delete'),
    path('game/edit/<slug:slug>/', views.GameEdit.as_view(), name='game_edit'),
    path('ranking-table/', views.RankingTable.as_view(), name='ranking_table'),
    path('csv-file-upload/', views.CSVFileUpload.as_view(), name='csv_file_upload'),

]
