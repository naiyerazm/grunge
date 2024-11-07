from uuid import UUID

from furl import furl
from rest_framework import status
from rest_framework.reverse import reverse as drf_reverse

from . import BaseAPITestCase


class TrackTests(BaseAPITestCase):
    def setUp(self):
        self.track_name = "Aim High"
        self.track_uuid = UUID("72e38ec1-306f-4de5-b485-409b5f877888")
        self.album_uuid = UUID("94892d51-dee4-42db-9593-d30a058220aa")

    def test_list_tracks(self):
        url = drf_reverse("track-list", kwargs={"version": self.version})
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["count"], 2783)

    def test_search_tracks(self):
        url = drf_reverse("track-list", kwargs={"version": self.version})
        url = furl(url).set({"name": self.track_name}).url
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["count"], 1)
        self.assertEqual(r.data["results"][0]["uuid"], self.track_uuid)

    def test_get_track(self):
        url = drf_reverse(
            "track-detail", kwargs={"version": self.version, "uuid": self.track_uuid}
        )
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["name"], self.track_name)
        self.assertEqual(r.data["album"]["uuid"], self.album_uuid)
