from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from movieapi.models.liked_movie import LikedMovie
from movieapi.serializers import LikedMovieSerializer

class MarkAsWatchedView(APIView):
    def patch(self, request, movie_id):
        try:
            # Retrieve the liked movie instance for the current user
            liked_movie = LikedMovie.objects.get(movie_id=movie_id, user=request.user)
        except LikedMovie.DoesNotExist:
            return Response({'error': 'Liked movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get the watched status from the request data
        watched_status = request.data.get('watched')
        
        if watched_status is None:
            return Response({'error': 'Watched status not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the watched status
        liked_movie.watched = watched_status
        liked_movie.save()
        
        # Serialize the updated instance and return it
        serializer = LikedMovieSerializer(liked_movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
