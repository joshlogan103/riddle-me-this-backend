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

class ParticipationListByProfile(generics.ListAPIView):
  serializer_class = ParticipationSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    profile = self.kwargs['profile_id']
    return Participation.objects.filter(profile=profile)

class ParticipationListByHuntInstance(generics.ListAPIView):
  serializer_class = ParticipationSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    hunt_instance = self.kwargs['hunt_instance_id']
    return Participation.objects.filter(hunt_instance=hunt_instance)
  
class ParticipationCreate(generics.ListCreateAPIView):
  serializer_class = ParticipationSerializer
  permission_classes = [permissions.IsAuthenticated]

  def perform_create(self, serializer):
    profile = self.kwargs['profile_id']
    hunt_instance = self.kwargs['hunt_instance_id']
    serializer.save(hunt_instance = hunt_instance, profile = profile)

class ParticipationDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ParticipationSerializer
  permission_classes = [permissions.IsAuthenticated]
  lookup_field = 'id'

  





