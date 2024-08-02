import logging
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from movieapi.models.user_movie import UserMovie
from movieapi.serializers import UserMovieSerializer

logger = logging.getLogger(__name__)

class UserMovieView(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            user_movie = UserMovie()
            user_movie.user_id = request.data['user_id']
            user_movie.movie_id = request.data['movie_id']
            user_movie.save()

            serialized = UserMovieSerializer(user_movie, many=False)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            logger.error(f"Key error: {e}")
            return Response({'message': f'Missing key: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            user_movies = UserMovie.objects.all()
            serializer = UserMovieSerializer(user_movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            user_movie = UserMovie.objects.get(pk=pk)
            serializer = UserMovieSerializer(user_movie, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserMovie.DoesNotExist:
            return Response({'message': 'UserMovie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            user_movie = UserMovie.objects.get(pk=pk)
            user_movie.user_id = request.data['user_id']
            user_movie.movie_id = request.data['movie_id']
            user_movie.watched = request.data['watched']
            user_movie.save()
            serializer = UserMovieSerializer(user_movie, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserMovie.DoesNotExist:
            return Response({'message': 'UserMovie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            user_movie = UserMovie.objects.get(pk=pk)
            user_movie.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except UserMovie.DoesNotExist:
            return Response({'message': 'UserMovie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
