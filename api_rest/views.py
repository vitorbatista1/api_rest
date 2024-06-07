from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, RegistroDeUsuarios
from .serializers import UserSerializer, UsersSerializers



@api_view(['GET'])
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def get_by_nick(request, nick):
    try:
        user = User.objects.get(pk=nick)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_manager(request):
    if request.method == 'GET':
        user_nickname = request.GET.get('user')
        if user_nickname:
            try:
                user = User.objects.get(pk=user_nickname)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        new_user = request.data
        user_nickname = new_user.get('user_nickname')
        user_email = new_user.get('user_email')

        if not user_nickname or not user_email:
            return Response({"error": "user_nickname and user_email are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(user_nickname=user_nickname).exists():
            return Response({
                "message": "User with this nickname already exists",
            }, status=status.HTTP_200_OK)

        if User.objects.filter(user_email=user_email).exists():
            return Response({
                "message": "User with this email already exists",
            }, status=status.HTTP_200_OK)

        serializer = UserSerializer(data=new_user)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User created successfully",
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)