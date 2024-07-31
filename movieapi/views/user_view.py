from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class UserView(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user = User()
        user.name = request.data['name']
        user.email = request.data['email']
        user.save()

        serialized = UserSerializer(user, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
