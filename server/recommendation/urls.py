from django.urls import path
from . import views

app_name='recommendation'

urlpatterns = [
    path('<str:partycode>/', views.recommendation_home, name='recommendation_home')
]
