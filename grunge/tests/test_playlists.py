from uuid import UUID

from furl import furl
from rest_framework import status
from rest_framework.reverse import reverse as drf_reverse
from unittest import skip

from . import BaseAPITestCase


class PlaylistTests(BaseAPITestCase):
    def setUp(self):
        self.playlist_name = "Playlist 1"
        self.playlist_uuid = UUID("392efbbd-80d7-4589-8d50-ef276ef26401")
        self.playlist_track_ids = [1,2]
        self.playlist_track_id = [2]

    def test_list_playlists(self):
        url = drf_reverse("playlist-list", kwargs={"version": self.version})
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["count"], 3)

    def test_search_playlists(self):
        url = drf_reverse("playlist-list", kwargs={"version": self.version})
        url = furl(url).set({"name": self.playlist_name}).url
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["count"], 1)
        self.assertEqual(r.data["results"][0]["uuid"], self.playlist_uuid)

    def test_get_playlist(self):
        url = drf_reverse(
            "playlist-detail", kwargs={"version": self.version, "uuid": self.playlist_uuid}
        )
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["name"], self.playlist_name)

    def test_create_playlist(self):
        url = drf_reverse(
            "playlist-list", kwargs={"version": self.version}
        )
        data = {"name":"Playlist Test","tracks":self.playlist_track_ids}
        r = self.client.post(url,data=data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_update_playlist(self):
        url = drf_reverse(
            "playlist-detail", kwargs={"version": self.version, "uuid": self.playlist_uuid}
        )
        data = {"name":"Playlist Test","tracks":self.playlist_track_id}
        r = self.client.put(url,data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_delete_playlist(self):
        url = drf_reverse(
            "playlist-detail", kwargs={"version": self.version, "uuid": self.playlist_uuid}
        )
        r = self.client.delete(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)