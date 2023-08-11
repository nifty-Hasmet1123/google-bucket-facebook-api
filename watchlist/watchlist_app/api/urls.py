from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (
    WatchListAv, 
    WatchListDetailAV, 
    StreamPlatformAV, 
    ReviewListAv, 
    ReviewCreate, 
    StreamWatchListView
)


router = DefaultRouter()

router.register("stream", StreamPlatformAV, basename = "stream-platform")

urlpatterns = [
    path("list/", WatchListAv.as_view(), name = "watch-list"),
    path("<int:pk>/", WatchListDetailAV.as_view(), name = "watchlist-detail"),
    path("", include(router.urls)),
    path("stream/reviews/", ReviewListAv.as_view(), name = "review-list"),
    path("stream/<int:platform_pk>/watchlist/<int:watchlist_pk>/review-create/", ReviewCreate.as_view(), name = "review-create"),
    path("stream/<int:platform_pk>/watchlist/<int:watchlist_pk>/", StreamWatchListView.as_view(), name = "streamwatchlist-detail")
]