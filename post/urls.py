from django.urls import path

from .views import Board

urlpatterns = [
    path('', Board.as_view()),
]