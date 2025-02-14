# from django.contrib import admin
# from django.urls import include, path
# from rest_framework import routers

# router = routers.DefaultRouter(trailing_slash=False)

# urlpatterns = [
#     path('', include(router.urls)),
# ]

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movieapi.views import register_user, login_user, MovieView, UserView, UserMovieView, GenreView, LikedMovieView, MarkAsWatchedView
from django.conf.urls import include


# router = DefaultRouter(trailing_slash=False)
router = DefaultRouter()
router.register(r'movies', MovieView, basename='movie')
router.register(r'users', UserView, basename='user')
router.register(r'usermovies', UserMovieView, basename='usermovie')
router.register(r'genres', GenreView, basename='genre')
router.register(r'likedmovies', LikedMovieView, basename='likedmovie')
# router.register(r'watched', MarkAsWatchedView, basename="markwatched")

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('likedmovies/<int:movie_id>/mark_watched/', MarkAsWatchedView.as_view(), name='mark-watched'),
]
