from uuid import UUID

from furl import furl
from rest_framework import status
from rest_framework.reverse import reverse as drf_reverse

from . import BaseAPITestCase


class ArtistTests(BaseAPITestCase):
    def setUp(self):
        self.artist_name = "Melvins"
        self.artist_uuid = UUID("dd1847a4-6743-4624-9fba-9f3ca54ccb28")

    def test_list_artists(self):
        url = drf_reverse("artist-list", kwargs={"version": self.version})
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["count"], 23)

    def test_search_artists(self):
        url = drf_reverse("artist-list", kwargs={"version": self.version})
        url = furl(url).set({"name": self.artist_name}).url
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["count"], 1)
        self.assertEqual(r.data["results"][0]["uuid"], self.artist_uuid)

    def test_get_artist(self):
        url = drf_reverse(
            "artist-detail", kwargs={"version": self.version, "uuid": self.artist_uuid}
        )
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["name"], self.artist_name)
