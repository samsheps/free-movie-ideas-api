from rest_framework import serializers
from .models.movie import Movie
from .models.genre import Genre
from .models.user_movie import UserMovie

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')

class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=False)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'release_year', 'info', 'director', 'watch_location', 'genre')

class UserMovieSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()  # Include the nested MovieSerializer

    class Meta:
        model = UserMovie
        fields = ['id', 'user', 'movie', 'watched']