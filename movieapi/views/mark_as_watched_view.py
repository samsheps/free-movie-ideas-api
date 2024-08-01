from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from movieapi.models.liked_movie import LikedMovie
from movieapi.serializers import LikedMovieSerializer

class MarkAsWatchedView(APIView):
    def patch(self, request, movie_id):
        try:
            liked_movie = LikedMovie.objects.get(movie_id=movie_id, user=request.user)
            liked_movie.watched = True
            liked_movie.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except LikedMovie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
