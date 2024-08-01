from rest_framework import serializers
from .models.movie import Movie
from .models.genre import Genre
from .models.user_movie import UserMovie
from .models.liked_movie import LikedMovie

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')

class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'release_year', 'info', 'director', 'watch_location', 'genre')

class UserMovieSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()  # Include the nested MovieSerializer

    class Meta:
        model = UserMovie
        fields = ['id', 'user', 'movie']

class LikedMovieSerializer(serializers.ModelSerializer):
    # Include the fields from MovieSerializer directly here
    id = serializers.IntegerField(source='movie.id')
    title = serializers.CharField(source='movie.title')
    release_year = serializers.IntegerField(source='movie.release_year')
    info = serializers.CharField(source='movie.info')
    director = serializers.CharField(source='movie.director')
    watch_location = serializers.CharField(source='movie.watch_location')
    genre = GenreSerializer(source='movie.genre')

    class Meta:
        model = LikedMovie
        fields = ('id', 'title', 'release_year', 'info', 'director', 'watch_location', 'genre', 'watched')

      