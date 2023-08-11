from watchlist_app.models import WatchList
from watchlist_app.api.serializer import WatchListSerializer
from rest_framework import mixins
from rest_framework import generics
# from rest_framework.views import APIView
# from django.shortcuts import get_object_or_404
# from rest_framework.response import Response

class WatchListAv(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    Ordered by platform.
    """
    queryset = WatchList.objects.all().order_by("platform")
    serializer_class = WatchListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class WatchListDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


# class WatchListDetailAV(APIView):
#     def get(self, request, pk):
#         queryset = WatchList.objects.all()
#         watchlist = get_object_or_404(queryset, pk = pk)

#         serializer = WatchListSerializer(watchlist)

#         return Response(serializer.data)
        