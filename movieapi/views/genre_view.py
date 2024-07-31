import logging
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from movieapi.models.genre import Genre
from movieapi.serializers import GenreSerializer

logger = logging.getLogger(__name__)

class GenreView(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            genre = Genre()
            genre.name = request.data['name']
            genre.save()

            serialized = GenreSerializer(genre, many=False)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            logger.error(f"Key error: {e}")
            return Response({'message': f'Missing key: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            genres = Genre.objects.all()
            serializer = GenreSerializer(genres, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Genre.DoesNotExist:
            return Response({'message': 'Genre not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            genre = Genre.objects.get(pk=pk)
            genre.name = request.data['name']
            genre.save()
            serializer = GenreSerializer(genre, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Genre.DoesNotExist:
            return Response({'message': 'Genre not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            genre = Genre.objects.get(pk=pk)
            genre.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Genre.DoesNotExist:
            return Response({'message': 'Genre not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
