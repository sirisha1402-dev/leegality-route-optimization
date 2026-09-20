from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .algorithms import dijkstra
from .models import Node, Edge, RouteHistory
from .serializers import (
    NodeSerializer,
    EdgeSerializer,
    RouteHistorySerializer,
)


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all().order_by("id")
    serializer_class = NodeSerializer


class EdgeViewSet(viewsets.ModelViewSet):
    queryset = Edge.objects.select_related(
        "source",
        "destination"
    ).all().order_by("id")

    serializer_class = EdgeSerializer


class RouteViewSet(viewsets.ViewSet):

    @action(
        detail=False,
        methods=["post"],
        url_path="shortest"
    )
    def shortest(self, request):

        source_name = request.data.get("source")
        destination_name = request.data.get("destination")

        # Validate request
        if not source_name or not destination_name:
            return Response(
                {
                    "error": "Source and destination are required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        source_name = source_name.strip()
        destination_name = destination_name.strip()

        # Find source node
        try:
            source = Node.objects.get(name=source_name)
        except Node.DoesNotExist:
            return Response(
                {
                    "error": "Source node does not exist."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Find destination node
        try:
            destination = Node.objects.get(
                name=destination_name
            )
        except Node.DoesNotExist:
            return Response(
                {
                    "error": "Destination node does not exist."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Build graph from database
        nodes = Node.objects.all()

        graph = {
            node.name: []
            for node in nodes
        }

        edges = Edge.objects.select_related(
            "source",
            "destination"
        )

        for edge in edges:
            graph[edge.source.name].append(
                (
                    edge.destination.name,
                    edge.latency
                )
            )

        # Run Dijkstra
        result = dijkstra(
            graph,
            source.name,
            destination.name
        )

        # No path
        if result is None:
            return Response(
                {
                    "error": (
                        f"No path exists between "
                        f"{source_name} and "
                        f"{destination_name}"
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Save successful route to history
        RouteHistory.objects.create(
            source=source,
            destination=destination,
            total_latency=result["total_latency"],
            path=result["path"],
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class RouteHistoryViewSet(
    viewsets.ReadOnlyModelViewSet
):

    queryset = RouteHistory.objects.select_related(
        "source",
        "destination"
    ).all()

    serializer_class = RouteHistorySerializer