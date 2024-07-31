import logging
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from movieapi.models.movie import Movie
from movieapi.models.genre import Genre
from movieapi.serializers import MovieSerializer
from movieapi.models.user_movie import UserMovie

logger = logging.getLogger(__name__)

class MovieView(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            chosen_genre = Genre.objects.get(pk=request.data['genre'])

            movie = Movie()
            movie.title = request.data['title']
            movie.genre = chosen_genre
            movie.release_year = request.data['release_year']
            movie.info = request.data['info']
            movie.director = request.data['director']
            movie.watch_location = request.data['watch_location']
            movie.save()

            user_movie = UserMovie()
            user_movie.user = request.user
            user_movie.movie = movie
            user_movie.watched = False  # or set it based on request data if needed
            user_movie.save()

            serialized = MovieSerializer(movie, many=False)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except Genre.DoesNotExist:
            logger.error("Genre does not exist")
            return Response({'message': 'Genre does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            logger.error(f"Key error: {e}")
            return Response({'message': f'Missing key: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def list(self, request):
    #         movies = Movie.objects.all()
    #         serializer = MovieSerializer(movies, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         logger.error(f"Unexpected error: {e}")
    #         return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#can import the movieserializer into either view 

    def list(self, request):
        try:
            # Check if the request is for user-specific movies
            # user_movies = request.query_params.get('user_movies', 'false').lower() == 'true'
            user_movies = request.query_params.get('owner')
            #this is setting the value of user movies to current

            if user_movies == 'current':
                # List movies for the authenticated user
                user_movie_ids = UserMovie.objects.filter(user=request.user).values_list('movie_id', flat=True)
                movies = Movie.objects.filter(id__in=user_movie_ids)
            else:
                # List all movies
                movies = Movie.objects.all()
            
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            movie = Movie.objects.get(pk=pk)
            chosen_genre = Genre.objects.get(pk=request.data['genre'])
            movie.title = request.data['title']
            movie.genre = chosen_genre
            movie.release_year = request.data['release_year']
            movie.info = request.data['info']
            movie.director = request.data['director']
            movie.watch_location = request.data['watch_location']
            movie.save()
            serializer = MovieSerializer(movie, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Genre.DoesNotExist:
            return Response({'message': 'Genre not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            movie = Movie.objects.get(pk=pk)
            movie.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# import logging
# from rest_framework.viewsets import ViewSet
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from movieapi.models.movie import Movie
# from movieapi.models.user_movie import UserMovie
# from movieapi.serializers import MovieSerializer

# logger = logging.getLogger(__name__)

# class MovieView(ViewSet):
#     permission_classes = [IsAuthenticated]

#     def create(self, request):
#         try:
#             chosen_genre = Genre.objects.get(pk=request.data['genre'])

#             movie = Movie()
#             movie.title = request.data['title']
#             movie.genre = chosen_genre
#             movie.release_year = request.data['release_year']
#             movie.info = request.data['info']
#             movie.director = request.data['director']
#             movie.watch_location = request.data['watch_location']
#             movie.save()

#             serialized = MovieSerializer(movie, many=False)
#             return Response(serialized.data, status=status.HTTP_201_CREATED)
#         except Genre.DoesNotExist:
#             logger.error("Genre does not exist")
#             return Response({'message': 'Genre does not exist'}, status=status.HTTP_400_BAD_REQUEST)
#         except KeyError as e:
#             logger.error(f"Key error: {e}")
#             return Response({'message': f'Missing key: {e}'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             logger.error(f"Unexpected error: {e}", exc_info=True)
#             return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def list(self, request):
#         try:
#             user_movies = request.query_params.get('owner')

#             if user_movies == 'current':
#                 # List movies for the authenticated user
#                 user_movie_ids = UserMovie.objects.filter(user=request.user).values_list('movie_id', flat=True)
#                 movies = Movie.objects.filter(id__in=user_movie_ids)
#             else:
#                 # List all movies
#                 movies = Movie.objects.all()
            
#             serializer = MovieSerializer(movies, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             logger.error(f"Unexpected error: {e}")
#             return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def retrieve(self, request, pk=None):
#         try:
#             movie = Movie.objects.get(pk=pk)
#             serializer = MovieSerializer(movie, many=False)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Movie.DoesNotExist:
#             return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             logger.error(f"Unexpected error: {e}")
#             return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def update(self, request, pk=None):
#         try:
#             movie = Movie.objects.get(pk=pk)
#             chosen_genre = Genre.objects.get(pk=request.data['genre'])
#             movie.title = request.data['title']
#             movie.genre = chosen_genre
#             movie.release_year = request.data['release_year']
#             movie.info = request.data['info']
#             movie.director = request.data['director']
#             movie.watch_location = request.data['watch_location']
#             movie.save()
#             serializer = MovieSerializer(movie, many=False)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Movie.DoesNotExist:
#             return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Genre.DoesNotExist:
#             return Response({'message': 'Genre not found'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             logger.error(f"Unexpected error: {e}")
#             return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def destroy(self, request, pk=None):
#         try:
#             movie = Movie.objects.get(pk=pk)
#             movie.delete()
#             return Response(None, status=status.HTTP_204_NO_CONTENT)
#         except Movie.DoesNotExist:
#             return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             logger.error(f"Unexpected error: {e}")
#             return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
