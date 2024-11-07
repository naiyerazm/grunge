from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from .views import Login, Logout, Artists, Albums, Tracks, Playlists
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login/',Login.as_view()),
    path('logout/',Logout.as_view()),

    path('artist/',Artists.as_view()),
    path('artist/list/',Artists.as_view()),
    path('artist/<uuid>',Artists.as_view()),
    path('artist/get-artist/<uuid>',Artists.get_artist_info),

    path('album/',Albums.as_view()),
    path('album/list/',Albums.as_view()),
    path('album/get-album/<uuid>',Albums.get_album_info),

    path('track/',Tracks.as_view()),
    path('track/list/',Tracks.as_view()),
    path('track/get-track/<uuid>',Tracks.get_track_info),

    path('playlist/',Playlists.as_view()),
    path('playlist/list/',Playlists.as_view()),
    # path('playlist/<uuid>',Playlists.as_view()),
    path('playlist/get-playlist/<uuid>',Playlists.get_playlist_info),
    
]