from django.urls import path, include
# from imdb.watchlist_app.api.views import ReviewDetail
# from watchlist_app.api.views import movie_list, movie_details
from rest_framework.routers import DefaultRouter

from watchlist_app.api.views import (ReviewDetail, WatchlistListView, WatchlistDetailView, StreamingViewSet,
                StreamingListView, StreamingListDetailView, ReviewList, ReviewCreate, UserReview, WatchlistGV)

router = DefaultRouter()
router.register('stream', StreamingViewSet ,basename="streamingplatform")


urlpatterns = [
    path('list/', WatchlistListView.as_view(), name='movie-list'),
    path('<int:pk>/', WatchlistDetailView.as_view(), name='movie-detail'),
    path('list2/', WatchlistGV.as_view(), name='watchlist-detail'),
    # path('stream/', StreamingListView.as_view(), name='stream-list'),
    # path('stream/<int:pk>', StreamingListDetailView.as_view(), name='streamingservice-detail'),
    path('', include(router.urls)),


    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('review/<int:pk>/',  ReviewDetail.as_view(), name='review-detail'),

    path('reviews/',  UserReview.as_view(), name='user-review-detail'),
]
# <str:username>/