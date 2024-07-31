from django.contrib.auth.models import User
from django.db import models

class UserMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies')
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='users')
    watched = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {self.movie.title}"
