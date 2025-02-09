from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_dataset, name='show_dataset'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('leaderboard/', views.get_leaderboard, name='get_leaderboard'),
    path('status/<int:problem_id>/', views.toggle_problem_status, name='toggle_status'),
    path('category/<int:problem_id>/', views.submit_category, name='submit_category'),
]
