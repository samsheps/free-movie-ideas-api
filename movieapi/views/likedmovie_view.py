from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from movieapi.models.liked_movie import LikedMovie
from movieapi.serializers import LikedMovieSerializer

class LikedMovieView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LikedMovieSerializer

    def get_queryset(self):
        user = self.request.user
        return LikedMovie.objects.filter(user=user)

    def create(self, request):
        user = request.user
        movie_id = request.data.get('movie_id')

        if LikedMovie.objects.filter(user=user, movie_id=movie_id).exists():
            return Response({'detail': 'Movie already in watchlist'}, status=status.HTTP_400_BAD_REQUEST)

        liked_movie = LikedMovie(user=user, movie_id=movie_id, watched=False)
        liked_movie.save()
        serializer = self.get_serializer(liked_movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        user = request.user
        movie_id = pk

        try:
            liked_movie = LikedMovie.objects.get(user=user, movie_id=movie_id)
            liked_movie.delete()
            return Response({'detail': 'Movie removed from watchlist'}, status=status.HTTP_204_NO_CONTENT)
        except LikedMovie.DoesNotExist:
            return Response({'detail': 'Movie not found in watchlist'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        user = request.user
        movie_id = pk
        watched = request.data.get('watched', False)

        try:
            liked_movie = LikedMovie.objects.get(user=user, movie_id=movie_id)
            liked_movie.watched = watched
            liked_movie.save()
            serializer = self.get_serializer(liked_movie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except LikedMovie.DoesNotExist:
            return Response({'detail': 'Movie not found in watchlist'}, status=status.HTTP_404_NOT_FOUND)
