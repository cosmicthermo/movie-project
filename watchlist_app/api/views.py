# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from watchlist_app.api.pagination import WatchlistPagination, WatchlistLimitPagination

from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from watchlist_app.models import Watchlist, StreamingService, Review
from watchlist_app.api.serializers import WatchlistSerializer, StreamingServiceSerializer, ReviewSerializer
from watchlist_app.api.throttles import ReviewCreateThrottle, ReviewListThrottle


class WatchlistGV(generics.ListAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer

    pagination_class = WatchlistLimitPagination
    # ordering_field = ['avg_rating']




class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # username = self.kwargs['username']
        
        username = self.request.query_params.get('username')
        # if username is not None:
        #     queryset = Review.objects.filter(review_user__username=username)
        return Review.objects.filter(review_user__username=username)
        # Review.objects.filter(review_user__username=username)



class StreamingViewSet(viewsets.ModelViewSet):
    queryset = StreamingService.objects.all()
    serializer_class = StreamingServiceSerializer

    permission_classes = [AdminOrReadOnly]



class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializers):
        pk = self.kwargs.get('pk')
        watchlist = Watchlist.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError('You have created this review!')

        if watchlist.numb_rating == 0:
            watchlist.avg_rating = serializers.validated_data['rating']
        else:
            watchlist.avg_rating =  (watchlist.avg_rating + serializers.validated_data['rating']) / 2
        
        watchlist.numb_rating = watchlist.numb_rating + 1
        watchlist.save() #### Damn the bug!!!

        serializers.save(watchlist=watchlist, review_user=review_user)




class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)



class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]

# class ReviewDetail(generics.GenericAPIView,
#                     mixins.RetrieveModelMixin):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewViewmodel(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class StreamingListView(APIView):
    def get(self, request):
        streaming_service = StreamingService.objects.all()
        serializers = StreamingServiceSerializer(streaming_service, many=True, context={'request': request})
        return Response(serializers.data)

    def post(self, request):
        serializers = StreamingServiceSerializer(data=request.data)
        if serializers.is_valid(): #raise_exception=True
            serializers.save()
            return Response(serializers.data)
        else: 
            return Response(serializers.errors)


class StreamingListDetailView(APIView):
    def get(self, request, pk):
        try:
            movie = StreamingService.objects.get(pk=pk)
        except StreamingService.DoesNotExist:
            return Response({'ErrorResponse': 'StreamingService not found'}, status=status.HTTP_404_NOT_FOUND)

        serializers = StreamingServiceSerializer(movie, context={'request': request})
        return Response(serializers.data)

    def put(self, request, pk):
        movie = StreamingService.objects.get(pk=pk)        
        serializers = StreamingServiceSerializer(movie, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else: 
            return Response(serializers.errors)


    def delete(self, request, pk):
        movie = StreamingService.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class WatchlistListView(APIView):
    def get(self, request):
        movies = Watchlist.objects.all()
        serializers = WatchlistSerializer(movies, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializers = WatchlistSerializer(data=request.data)
        if serializers.is_valid(): #raise_exception=True
            serializers.save()
            return Response(serializers.data)
        else: 
            return Response(serializers.errors)

class WatchlistDetailView(APIView):
    def get(self, request, pk):
        try:
            movie = Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            return Response({'ErrorResponse': 'Watchlist not found'}, status=status.HTTP_404_NOT_FOUND)

        serializers = WatchlistSerializer(movie)
        return Response(serializers.data)

    def put(self, request, pk):
        movie = Watchlist.objects.get(pk=pk)        
        serializers = WatchlistSerializer(movie, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else: 
            return Response(serializers.errors)


    def delete(self, request, pk):
        movie = Watchlist.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    



# class StreamingViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     def list(self, request):
#         queryset = StreamingService.objects.all()
#         serializer = StreamingServiceSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamingService.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = StreamingServiceSerializer(user)
#         return Response(serializer.data)






# @api_view(['GET', 'POST'])
# def movie_list(request):

#     if request.method == 'GET':
#         movies = Watchlist.objects.all()
#         serializers = WatchlistSerializer(movies, many=True)
#         return Response(serializers.data)

#     if request.method == 'POST':
#         serializers = WatchlistSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data)
#         else: 
#             return Response(serializers.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):

#     if request.method == 'GET':
#         try:
#             movie = Watchlist.objects.get(pk=pk)
#         except Watchlist.DoesNotExist:
#             return Response({'ErrorResponse': 'Watchlist not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializers = WatchlistSerializer(movie)
#         return Response(serializers.data)

#     if request.method == 'PUT':
#         movie = Watchlist.objects.get(pk=pk)        
#         serializers = WatchlistSerializer(movie, data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data)
#         else: 
#             return Response(serializers.errors)

#     if request.method == 'DELETE':
#         movie = Watchlist.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)