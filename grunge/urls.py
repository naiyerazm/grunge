from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from .viewsets import AlbumViewSet, ArtistViewSet, TrackViewSet, PlaylistViewSet
from django.conf.urls.static import static

urlpatterns = []


if settings.DJANGO_ADMIN_ENABLED:
    urlpatterns += [
        re_path("^$", RedirectView.as_view(url="/admin/", permanent=True)),
        path("admin/", admin.site.urls),
    ]

if settings.DJANGO_API_ENABLED:
    api_router = DefaultRouter(trailing_slash=False)
    api_router.register("artists", ArtistViewSet)
    api_router.register("albums", AlbumViewSet)
    api_router.register("tracks", TrackViewSet)
    api_router.register("playlists", PlaylistViewSet)

    urlpatterns += [
        path("api/<version>/", include(api_router.urls)),
    ]

urlpatterns += [
        path("user/", include('user.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
