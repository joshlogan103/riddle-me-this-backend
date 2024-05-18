from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from ..serializers import ProfileSerializer, ParticipationSerializer
from ..models import Profile, Participation

class ProfileList(generics.ListCreateAPIView):
  serializer_class = ProfileSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    return Profile.objects.filter(user=user)
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ProfileSerializer
  lookup_field = 'id'

  def get_queryset(self):
    user = self.request.user
    return Profile.objects.filter(user=user)
  
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, context = {'request': request})

    participations = Participation.objects.filter(profile=instance.id)
    participations_serializer = ParticipationSerializer(participations, many = True, context = {'request': request})

    

