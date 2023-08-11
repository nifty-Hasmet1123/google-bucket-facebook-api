from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class StreamPlatform(models.Model):
    stream_platform = models.CharField(max_length = 50, unique = True)
    about = models.CharField(max_length = 200)
    website = models.URLField(max_length = 200, unique = True)

    def __str__(self):
        return self.stream_platform

class WatchList(models.Model):
    title = models.CharField(max_length = 50, unique = True)
    storyline = models.CharField(max_length = 50)
    active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True)
    platform = models.ForeignKey(
        StreamPlatform,
        on_delete = models.CASCADE,
        to_field = "stream_platform",
        related_name = "platform_watchlist"
    )

    def __str__(self):
        return self.title
    
class Review(models.Model):
    rating = models.PositiveIntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(5)]
    )

    description = models.CharField(max_length = 200)
    active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True)
    update = models.DateTimeField(auto_now = True)
    watchlist_review = models.ForeignKey(
        WatchList,
        on_delete = models.CASCADE,
        related_name = "reviews"
    )

    def __str__(self):
        return f"{self.rating} | {self.watchlist_review.title}"