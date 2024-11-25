from django.urls import path
from youtube_notes.views import YouTubeNotes

yt_notes = YouTubeNotes()
urlpatterns = [
    path('', yt_notes.getYouTubeNotes),
    path('query', yt_notes.searchQuery),
]