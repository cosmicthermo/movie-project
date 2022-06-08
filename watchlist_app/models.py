from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.

class StreamingService(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=200)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class Watchlist(models.Model):
    title = models.CharField(max_length=50)
    avg_rating = models.FloatField(default=0)
    numb_rating = models.IntegerField(default=0)
    storyline = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    platform = models.ForeignKey(StreamingService, on_delete=models.CASCADE, related_name="watchlist")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    title = models.CharField(max_length=50)
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='review')
    description = models.CharField(max_length=1000)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating) + self.rating*" * " + " | " + self.watchlist.title