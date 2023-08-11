from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from watchlist_app.models import Review, WatchList
from watchlist_app.api.serializer import ReviewSerializer

class ReviewListAv(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # get_queryset is a special instance method from the ListAPIView
        pk = self.kwargs["pk"]
        
        return Review.objects.filter(watchlist_review = pk)
    
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        platform_pk = self.kwargs["platform_pk"]
        watchlist_pk = self.kwargs["watchlist_pk"]

        obj = get_object_or_404(
            klass = WatchList,
            pk = watchlist_pk
        )

        serializer.save(watchlist_review = obj)