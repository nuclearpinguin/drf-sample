from django.urls import path
from movies import views

urlpatterns = [
    path('movies/', views.MoviesList.as_view()),
    path('movies/<int:pk>/', views.MovieDetails.as_view()),
    path('comments/', views.CommentsList.as_view()),
    path('comments/<int:pk>/', views.CommentsForMovie.as_view()),
    path('top/', views.TopList.as_view()),
]
