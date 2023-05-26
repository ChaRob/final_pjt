from django.urls import path
from . import views
app_name = 'movies'

urlpatterns = [
    path('home/', views.home, name='movie_home'),
    path('top_rated/<int:pk>/', views.movie_list_top_rated, name='movie_list_top_rated'),
    path('popular/<int:pk>/', views.movie_list_popular, name='movie_list_popular'),
    path('boxoffice/', views.movie_list_boxoffice, name='movie_list_boxoffice'),
    path('genre/<int:genre_id>/<int:pk>/', views.movie_list_genre, name='movie_list_genre'),
    path('detail/<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('review/<int:movie_pk>/', views.review_list, name='review_list'),
    path('review/<int:movie_pk>/create/', views.create_review, name='create_review'),
    path('review/detail/<int:review_pk>/', views.review_detail, name='review_detail'),
    path('review/detail/<int:review_pk>/like/', views.like, name='review_like'),
    path('comment/<int:review_pk>/', views.comment_list, name='comment_list'),
    path('comment/<int:review_pk>/create/', views.create_comment, name='create_comment'),
    path('comment/update/<int:comment_pk>/', views.comment_update, name='comment_update'),
    path('search/<str:search_name>/', views.search, name='search'),
]
