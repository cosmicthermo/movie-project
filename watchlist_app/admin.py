from django.contrib import admin
from watchlist_app.models import Watchlist, StreamingService, Review

# Register your models here.
admin.site.register(Watchlist)
admin.site.register(StreamingService)
admin.site.register(Review)