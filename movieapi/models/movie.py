from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    release_year = models.IntegerField()
    info = models.TextField()
    director = models.CharField(max_length=255)
    watch_location = models.CharField(max_length=255)

    def __str__(self):
        return self.title