from django.core.validators import MaxLengthValidator, MaxValueValidator
from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(
        source = "watchlist.platform.stream_platform",
        read_only = True 
    )

    class Meta():
        model = Review
        exclude = ["watchlist_review"] # exclude this. this is not needed when creating review-creation

class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many = True, read_only = True)

    class Meta():
        model = WatchList
        fields = [
            "id",
            "title",
            "storyline",
            "active",
            "created",
            "platform",
            "reviews"
        ]

class StreamPlatformSerializer(serializers.ModelSerializer):
    platform_watchlist = WatchListSerializer(many = True, read_only = True)

    class Meta():
        model = StreamPlatform
        fields = [
            "id",
            "stream_platform",
            "about",
            "website",
            "platform_watchlist"
        ]



