from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data['email']
    password = request.data['password']

    authenticated_user = authenticate(username=email, password=password)

    if authenticated_user is not None:
        token, created = Token.objects.get_or_create(user=authenticated_user)
        logger.info(f'Token retrieved for user {authenticated_user.username}: {token.key}')
        data = {
            'valid': True,
            'token': token.key
        }
        return Response(data)
    else:
        logger.warning('Authentication failed for user with email %s', email)
        data = {'valid': False}
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''
    email = request.data.get('email', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    password = request.data.get('password', None)

    if email is not None\
        and first_name is not None \
        and last_name is not None \
        and password is not None:

        try:
            # Create a new user by invoking the create_user helper method
            # on Django's built-in User model
            new_user = User.objects.create_user(
                username=request.data['email'],
                email=request.data['email'],
                password=request.data['password'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name']
            )
        except IntegrityError:
            return Response(
                {'message': 'An account with that username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=new_user)
        # Return the token to the client
        data = { 'token': token.key }
        return Response(data)

    return Response({'message': 'You must provide email, password, first_name, and last_name'}, status=status.HTTP_400_BAD_REQUEST)