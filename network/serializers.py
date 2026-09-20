from rest_framework import serializers

from .models import Node, Edge, RouteHistory


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ["id", "name"]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Name is required.")

        return value


class EdgeSerializer(serializers.ModelSerializer):
    source = serializers.CharField()
    destination = serializers.CharField()

    class Meta:
        model = Edge
        fields = ["id", "source", "destination", "latency"]

    def validate(self, data):
        source_name = data["source"].strip()
        destination_name = data["destination"].strip()
        latency = data["latency"]

        if not source_name:
            raise serializers.ValidationError(
                {"source": "Source is required."}
            )

        if not destination_name:
            raise serializers.ValidationError(
                {"destination": "Destination is required."}
            )

        if latency <= 0:
            raise serializers.ValidationError(
                {"latency": "Latency must be greater than 0."}
            )

        try:
            source = Node.objects.get(name=source_name)
        except Node.DoesNotExist:
            raise serializers.ValidationError(
                {"source": "Source node does not exist."}
            )

        try:
            destination = Node.objects.get(name=destination_name)
        except Node.DoesNotExist:
            raise serializers.ValidationError(
                {"destination": "Destination node does not exist."}
            )

        if Edge.objects.filter(
            source=source,
            destination=destination
        ).exists():
            raise serializers.ValidationError(
                "This edge already exists."
            )

        data["source"] = source
        data["destination"] = destination

        return data

    def create(self, validated_data):
        return Edge.objects.create(**validated_data)


class RouteHistorySerializer(serializers.ModelSerializer):
    source = serializers.CharField(
        source="source.name",
        read_only=True
    )
    destination = serializers.CharField(
        source="destination.name",
        read_only=True
    )

    class Meta:
        model = RouteHistory
        fields = [
            "id",
            "source",
            "destination",
            "total_latency",
            "path",
            "created_at",
        ]