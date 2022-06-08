# from django.shortcuts import render
# from watchlist_app.models import Watchlist
# from django.http import JsonResponse
# # Create your views here.

# def movie_list(request):
#     movies = Watchlist.objects.all()
#     data = {
#         "movie": list(movies.values())
#     }
#     # print(movies)
#     # print(movies.values())
#     # print(list(movies.values()))
#     return JsonResponse(data)

# def movie_details(request, pk):
#     movie = Watchlist.objects.get(pk=pk)
#     data = {
#         'name': movie.name,
#         'description': movie.description,
#         'active': movie.active,
#     }
#     print(movie.description)

#     return JsonResponse(data)