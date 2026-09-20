from rest_framework import status
from rest_framework.test import APITestCase

from .models import Node, Edge, RouteHistory


class NetworkAPITestCase(APITestCase):

    def setUp(self):
        self.server_a = Node.objects.create(name="ServerA")
        self.server_b = Node.objects.create(name="ServerB")
        self.server_c = Node.objects.create(name="ServerC")
        self.server_d = Node.objects.create(name="ServerD")

    def test_create_node(self):
        response = self.client.post(
            "/nodes/",
            {"name": "ServerX"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["name"],
            "ServerX",
        )

    def test_duplicate_node(self):
        response = self.client.post(
            "/nodes/",
            {"name": "ServerA"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_create_edge(self):
        response = self.client.post(
            "/edges/",
            {
                "source": "ServerA",
                "destination": "ServerB",
                "latency": 12.5,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_invalid_latency(self):
        response = self.client.post(
            "/edges/",
            {
                "source": "ServerA",
                "destination": "ServerB",
                "latency": 0,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_shortest_route(self):
        Edge.objects.create(
            source=self.server_a,
            destination=self.server_b,
            latency=12.5,
        )

        Edge.objects.create(
            source=self.server_b,
            destination=self.server_d,
            latency=10.9,
        )

        Edge.objects.create(
            source=self.server_a,
            destination=self.server_c,
            latency=20,
        )

        Edge.objects.create(
            source=self.server_c,
            destination=self.server_d,
            latency=5,
        )

        response = self.client.post(
            "/routes/shortest/",
            {
                "source": "ServerA",
                "destination": "ServerD",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["path"],
            [
                "ServerA",
                "ServerB",
                "ServerD",
            ],
        )

        self.assertEqual(
            response.data["total_latency"],
            23.4,
        )

    def test_no_path(self):
        response = self.client.post(
            "/routes/shortest/",
            {
                "source": "ServerA",
                "destination": "ServerD",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_route_history_created(self):
        Edge.objects.create(
            source=self.server_a,
            destination=self.server_b,
            latency=10,
        )

        response = self.client.post(
            "/routes/shortest/",
            {
                "source": "ServerA",
                "destination": "ServerB",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            RouteHistory.objects.count(),
            1,
        )

    def test_route_history(self):
        Edge.objects.create(
            source=self.server_a,
            destination=self.server_b,
            latency=10,
        )

        self.client.post(
            "/routes/shortest/",
            {
                "source": "ServerA",
                "destination": "ServerB",
            },
            format="json",
        )

        response = self.client.get(
            "/routes/history/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )
