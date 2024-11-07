from uuid import UUID

from furl import furl
from rest_framework import status
from rest_framework.reverse import reverse as drf_reverse

from . import BaseAPITestCase


class AlbumTests(BaseAPITestCase):
    def setUp(self):
        self.album_name = "A Walk with Love & Death"
        self.album_uuid = UUID("94892d51-dee4-42db-9593-d30a058220aa")
        self.artist_uuid = UUID("dd1847a4-6743-4624-9fba-9f3ca54ccb28")

    def test_list_albums(self):
        url = drf_reverse("album-list", kwargs={"version": self.version})
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["count"], 229)

    def test_search_albums(self):
        url = drf_reverse("album-list", kwargs={"version": self.version})
        url = furl(url).set({"name": self.album_name}).url
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["count"], 1)
        self.assertEqual(r.data["results"][0]["uuid"], self.album_uuid)
        self.assertEqual(r.data["results"][0]["artist"]["uuid"], self.artist_uuid)

    def test_get_album(self):
        url = drf_reverse(
            "album-detail", kwargs={"version": self.version, "uuid": self.album_uuid}
        )
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["name"], self.album_name)
        self.assertEqual(r.data["artist"]["uuid"], self.artist_uuid)
