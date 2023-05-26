from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, InfoSerializer, ProfileSerializer
from .models import User
# Create your views here.

@api_view(['GET'])
def userinfo(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    serializer = InfoSerializer(user)
    return Response(serializer.data)

@api_view(['PUT'])
def update(request):
    user = User.objects.get(pk=request.user.pk)
    serializer = ProfileSerializer(user, data=request.data)
    if serializer.is_valid(raise_exception=False):
        serializer.save(user=request.user)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    print(serializer.errors)
    
@api_view(['POST'])
def follow(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if user.followers.filter(pk=request.user.pk).exists():
        user.followers.remove(request.user)
    else:
        user.followers.add(request.user)
    return Response(status=status.HTTP_200_OK)


