from rest_framework import viewsets,status
from django.shortcuts import get_object_or_404
from .filters import AlbumFilter, ArtistFilter, TrackFilter, PlaylistFilter, PlaylistTrackFilter
from .models import Album, Artist, Track, Playlist, PlaylistTrack
from .serializers import AlbumSerializer, ArtistSerializer, TrackSerializer, PlaylistSerializer, PlaylistTrackSerializer
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin


# class BaseAPIViewSet(LoginRequiredMixin,viewsets.ReadOnlyModelViewSet):
class BaseAPIViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"


class ArtistViewSet(BaseAPIViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filterset_class = ArtistFilter

    def create(self, request, **kwargs):
        try:
            name = request.data.get('name')
            data = {"name":name}
            serializer_context = {
                'request': request,
            }
            serializer = self.serializer_class(data=data,context=serializer_context)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'msg':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def update(self, request, *args, **kwargs):
        try:
            uuid = kwargs.pop('uuid', False)
            name = request.data.get('name')
            serializer_context = {
                'request': request,
            }
            if name is None or name == '':
                return Response(data={"name":["This field may not be blank."]},
                                status=status.HTTP_400_BAD_REQUEST)
            obj = Artist.objects.filter(uuid=uuid).first()
            obj.name = name
            obj.save()
            return Response(data=ArtistSerializer(obj,many=False,context=serializer_context).data,
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'msg':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, *args, **kwargs):
        try:
            uuid = kwargs.pop('uuid', False)
            serializer_context = {
                'request': request,
            }
            obj=Artist.objects.filter(uuid=uuid).first()
            data = ArtistSerializer(obj,context=serializer_context).data
            Artist.objects.filter(uuid=uuid).delete()
            return Response(data=data,
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'msg':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AlbumViewSet(BaseAPIViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filterset_class = AlbumFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("artist").prefetch_related("tracks")
    
    def create(self, request, **kwargs):
        try:
            name = request.data.get('name')
            year = request.data.get('year')
            artist = request.data.get('artist')
            tracks = request.data.get('tracks')
            errors = {}
            if name is None or name == "":
                errors["name"] = ["This field may not be blank."]
            if year is None or year == "":
                errors["year"] = ["This field may not be blank."]
            if artist is None or artist == "":
                errors["artist"] = ["This field may not be blank."]
            if tracks is None or len(tracks) == 0:
                errors["tracks"] = ["This field should have atleast one track"]
            if len(errors) > 0:
                return Response(data=errors,
                                status=status.HTTP_400_BAD_REQUEST)
            serializer_context = {
                'request': request,
            }
            obj = Album.objects.create(name=name,year=year,artist_id=artist['id'])
            if not obj:
                return Response(data={'msg':'There is server error'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            for track in tracks:
                Track.objects.create(name=track['name'],number=track['number'],album_id=obj.id)
            return Response(data=AlbumSerializer(obj,many=False,context=serializer_context).data,
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'msg':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, *args, **kwargs):
        try:
            uuid = kwargs.pop('uuid', False)
            name = request.data.get('name')
            year = request.data.get('year')
            artist = request.data.get('artist')
            tracks = request.data.get('tracks')
            errors = {}
            if name is None or name == "":
                errors["name"] = ["This field may not be blank."]
            if year is None or year == "":
                errors["year"] = ["This field may not be blank."]
            if artist is None or artist == "":
                errors["artist"] = ["This field may not be blank."]
            if tracks is None or len(tracks) == 0:
                errors["tracks"] = ["This field should have atleast one track"]
            if len(errors) > 0:
                return Response(data=errors,
                                status=status.HTTP_400_BAD_REQUEST)
            serializer_context = {
                'request': request,
            }
            obj = Album.objects.filter(uuid=uuid).first()
            obj.name = name
            obj.year = year
            obj.artist_id = artist['id']
            obj.save()
            Track.objects.filter(album_id=obj.id).delete()
            for track in tracks:
                Track.objects.create(name=track['name'],number=track['number'],album_id=obj.id)
            return Response(data=AlbumSerializer(obj,many=False,context=serializer_context).data,
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'msg':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, *args, **kwargs):
        try:
            uuid = kwargs.pop('uuid', False)
            serializer_context = {
                'request': request,
            }
            obj = Album.objects.filter(uuid=uuid).first()
            data = AlbumSerializer(obj,many=False,context=serializer_context).data
            Track.objects.filter(album_id=obj.id).delete()
            Album.objects.filter(uuid=uuid).delete()
            return Response(data=data,
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'msg':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TrackViewSet(BaseAPIViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    filterset_class = TrackFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("album", "album__artist")
    
    def create(self, request, **kwargs):
        try:
            name = request.data.get('name')
            number = request.data.get('number')
            album_id = request.data.get('album_id')
            errors = {}
            if name is None or name == "":
                errors["name"] = ["This field may not be blank."]
            if number is None or number == "":
                errors["number"] = ["This field may not be blank."]
            if album_id is None or album_id == "":
                errors["album_id"] = ["This field may not be blank."]
            
            if len(errors) > 0:
                return Response(data=errors,
                                status=status.HTTP_400_BAD_REQUEST)
            serializer_context = {
                'request': request,
            }
            obj = Track.objects.create(name=name,number=number,album_id=album_id)
            if obj:
                return Response(data=TrackSerializer(obj,many=False,context=serializer_context).data,
                                status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'msg':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, **kwargs):
        try:
            uuid = kwargs.pop('uuid', False)
            name = request.data.get('name')
            number = request.data.get('number')
            album_id = request.data.get('album_id')
            errors = {}
            if name is None or name == "":
                errors["name"] = ["This field may not be blank."]
            if number is None or number == "":
                errors["number"] = ["This field may not be blank."]
            if album_id is None or album_id == "":
                errors["album_id"] = ["This field may not be blank."]
            
            if len(errors) > 0:
                return Response(data=errors,
                                status=status.HTTP_400_BAD_REQUEST)
            serializer_context = {
                'request': request,
            }
            obj = Track.objects.filter(uuid=uuid).first()
            obj.name=name
            obj.number=number
            obj.album_id=album_id
            obj.save()
            if obj:
                return Response(data=TrackSerializer(obj,many=False,context=serializer_context).data,
                                status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'msg':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, **kwargs):
        try:
            uuid = kwargs.pop('uuid', False)
            serializer_context = {
                'request': request,
            }
            obj = Track.objects.filter(uuid=uuid).first()
            data = TrackSerializer(obj,many=False,context=serializer_context).data
            Track.objects.filter(uuid=uuid).delete()
            return Response(data=data,
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'msg':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlaylistViewSet(BaseAPIViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    filterset_class = PlaylistFilter

    def create(self, request, **kwargs):
        try:
            name = request.data.get('name',None)
            tracks = request.data.get('tracks',None)
            errors = {}
            if name is None or name == "":
                errors["name"] = ["This field may not be blank."]

            if len(tracks) == 0:
                errors["tracks"] = ["This field may not be blank."]

            if len(errors) > 0:
                return Response(data=errors,
                                status=status.HTTP_400_BAD_REQUEST)
            serializer_context = {
                'request': request,
            }
            obj = Playlist.objects.create(name=name)
            if obj:
                for track in tracks:
                    PlaylistTrack.objects.create(track_id=track,playlist_id=obj.id)
                playlist_serializer = PlaylistSerializer(obj,many=False,context=serializer_context).data
                return Response(data=playlist_serializer,
                                status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'msg':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, **kwargs):
        try:
            uuid = kwargs.pop('uuid', False)
            name = request.data.get('name',None)
            tracks = request.data.get('tracks',None)
            errors = {}
            if name is None or name == "":
                errors["name"] = ["This field may not be blank."]

            if len(tracks) == 0:
                errors["tracks"] = ["This field may not be blank."]

            if len(errors) > 0:
                return Response(data=errors,
                                status=status.HTTP_400_BAD_REQUEST)
            serializer_context = {
                'request': request,
            }
            obj = Playlist.objects.filter(uuid=uuid).first()
            obj.name = name
            obj.save()
            PlaylistTrack.objects.filter(playlist_id=obj.id).delete()
            if obj:
                for track in tracks:
                    PlaylistTrack.objects.create(track_id=track,playlist_id=obj.id)
                playlist_serializer = PlaylistSerializer(obj,many=False,context=serializer_context).data
                return Response(data=playlist_serializer,
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'msg':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, **kwargs):
        try:
            uuid = kwargs.pop('uuid', False)
            serializer_context = {
                'request': request,
            }
            obj = Playlist.objects.filter(uuid=uuid).first()
            data = PlaylistSerializer(obj,many=False,context=serializer_context).data
            Playlist.objects.filter(uuid=uuid).delete()
            PlaylistTrack.objects.filter(playlist_id=obj.id).delete()
            return Response(data=data,
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'msg':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)