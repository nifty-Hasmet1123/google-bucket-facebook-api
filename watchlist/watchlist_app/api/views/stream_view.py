from django.shortcuts import get_object_or_404
from watchlist_app.models import StreamPlatform, WatchList
from watchlist_app.api.serializer import StreamPlatformSerializer, WatchListSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

class StreamPlatformAV(viewsets.ViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many = True)

        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        queryset = StreamPlatform.objects.all()
        obj = get_object_or_404(queryset, pk = pk)
        
        serializer = StreamPlatformSerializer(obj)

        return Response(serializer.data)
    
    def create(self, request):
        serializer = StreamPlatformSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def update(self, request, pk):
        # both this and the commented code have the same functionality 
        # remember when using get_object_or_404 function you need to get the whole queryset 

        queryset = StreamPlatform.objects.all()
        obj = get_object_or_404(queryset, pk = pk)

        serializer = StreamPlatformSerializer(obj, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

        # try: 
        #     instance = StreamPlatform.objects.get(pk = pk)
        # except StreamPlatform.DoesNotExist:
        #     return Response({"detail": "not found"} status.http_400_BAD_REQUEST)
        


        # serializer = StreamPlatformSerializer(instance, data = request.data)

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        
        # return Response(serializer.errors)

    def delete(self, request, pk): 
        queryset = StreamPlatform.objects.all()
        obj = get_object_or_404(queryset, pk = pk)

        obj.delete()

        return Response(status.HTTP_204_NO_CONTENT)
    
        # or

        # queryset = StreamPlatform.objects.get(pk = pk)
        # queryset.delete()

        # return Response(status.httpno HTTP_204_NO_CONTENT)

# using APIView
class StreamWatchListView(APIView):
    def get(self, request, platform_pk, watchlist_pk):
        target_platform = get_object_or_404(StreamPlatform, pk = platform_pk)
        watchlist = get_object_or_404(WatchList, pk = watchlist_pk, platform = target_platform)
        
        serializer = WatchListSerializer(watchlist)

        return Response(serializer.data)


# using generic RetrieveAPIVIew
# class StreamWatchListView(generics.RetrieveAPIView):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = WatchListSerializer

#     def get_object(self):
#         platform_pk = self.kwargs["platform_pk"]
#         watchlist_pk = self.kwargs["watchlist_pk"]

#         # retrieve the stream platform based on platform_pk
#         target_platform = get_object_or_404(StreamPlatform, pk = platform_pk)

#         # retrieve the specific watchlist associated with streamplatform
#         result = get_object_or_404(WatchList, pk = watchlist_pk, platform = target_platform) # platform is a field in the WatchList class

#         return result