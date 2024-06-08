from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import json
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import *
import requests
from pathlib import Path
from django.core.files.base import ContentFile


@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def SignupView(request):
    email = request.data.get('email').lower()
    password = request.data.get('password')
    username = request.data.get('username')
    if not email or not password or not username:
        return Response({"error": "Username , Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email is already taken"}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, email=email, password=password)
    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def LoginView(request):
    ResponseData = None
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            ResponseData = { "token": token.key,"status": "200","message": "Login successful"}
    except Exception as e:
        ResponseData = {"status":"400","error": "Invalid credentials" }
    return Response(ResponseData)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchUsers(request):
    query = request.query_params.get('keyword', '')
    if query:
        if '@' in query:
            users = User.objects.filter(email__iexact=query)
        else:
            users = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
    else:
        users = User.objects.none()
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendFriendRequest(request):
    from_user_id = request.data.get('from_user_id') 
    to_user_id = request.data.get('to_user_id')
    try:
        from_user = User.objects.get(id=from_user_id)
        to_user = User.objects.get(id=to_user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

    last_minute = timezone.now() - timedelta(minutes=1)
    recent_requests =  FriendRequest.objects.filter(from_user=from_user, timestamp__gte=last_minute)
    if recent_requests.count() >= 3:
        return Response({'error': 'Cannot send more than 3 friend requests within a minute'}, status=status.HTTP_400_BAD_REQUEST)
    friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user,status='pending')
    return Response(FriendReqSerializer(friend_request).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respondFriendRequest(request, key):
    try:
        friend_request = get_object_or_404(FriendRequest, id=key, to_user=request.data.get('to_user_id'))  # Adjusted to_user identification for demo
        
        response_status = request.data.get('status')
        if response_status not in ['accepted', 'rejected']:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        
        friend_request.status = response_status
        friend_request.save()
        return Response(FriendReqSerializer(friend_request).data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listFriends(request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    friends = User.objects.filter(
        Q(sent_requests__to_user=user, sent_requests__status='accepted') |
        Q(received_requests__from_user=user, received_requests__status='accepted')
    ).distinct()
    
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listPendingRequests(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    pending_requests = FriendRequest.objects.filter(to_user=user, status='pending')
    serializer = FriendReqSerializer(pending_requests, many=True)
    return Response(serializer.data)




    
  
