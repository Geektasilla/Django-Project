
from django.urls import path
from django_app.views import greetings

greetings = [
    path('home-page/', greetings)
]
