from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from .models import Profile, Participation, HuntInstance, ScavengerHunt,RiddleItem
from .serializers import UserSerializer, ProfileSerializer, ParticipationSerializer, HuntInstanceSerializer, ScavengerHuntSerializer, RiddleItemSerializer

# Create your views here.
# CreatUserView, LoginView, VerifyUserView

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data
        })

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request): #POST method
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request): #GET method
        user = User.objects.get(username=request.user)
        refresh = RefreshToken.for_user(request.user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
    
class ProfileList(generics.ListCreateAPIView):
  serializer_class = ProfileSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    return Profile.objects.filter(user=user)
  
  def perform_create(self, serializer):
    user = self.request.user
    if Profile.objects.filter(user=user).exists():
        raise ValidationError(f"The user {user} already has a profile.")
    serializer.save(user=self.request.user)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context = {'request': request})

        participations = Participation.objects.filter(profile=instance.id)
        participations_serializer = ParticipationSerializer(participations, many = True, context = {'request': request})

        return Response({
            'profile': serializer.data,
            'participations': participations_serializer.data
        })

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


class HuntInstanceList(generics.ListCreateAPIView):
    serializer_class = HuntInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
       hunt_template = self.kwargs['hunt_template_id']
       return ScavengerHunt.objects.filter(scavenger_hunt = hunt_template)
    
    def perform_create(self, serializer):
        hunt_template = self.kwargs['hunt_template_id']
        serializer.save(scavenger_hunt = hunt_template)
        

class HuntInstanceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HuntInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context = {'request': request})
        
        hunt_template_id = self.kwargs['hunt_template_id']
        hunt_template = ScavengerHunt.objects.get(id = hunt_template_id)
        scavenger_hunt_serializer = ScavengerHuntSerializer(hunt_template, context = {'request': request})
        
        riddle_items = RiddleItem.objects.filter(scavenger_hunt = hunt_template_id)
        riddle_items_serializer = RiddleItemSerializer(riddle_items, many = True, context = {'request': request})

        return Response({
            'hunt_instance': serializer.data,
            'hunt_template': scavenger_hunt_serializer.data,
            'riddle_items': riddle_items_serializer.data
        })

class HuntTemplateList(generics.ListCreateAPIView):
    serializer_class = ScavengerHuntSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ScavengerHunt.objects.filter(creator = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(creator = self.request.user)

class HuntTemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScavengerHuntSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context = {'request': request})
        
        hunt_instances = HuntInstance.objects.filter(scavenger_hunt = instance.id)
        hunt_instances_serializer = HuntInstanceSerializer(hunt_instances, many = True, context = {'request': request})

        riddle_items = RiddleItem.objects.filter(scavenger_hunt = instance.id)
        riddle_items_serializer = RiddleItemSerializer(riddle_items, many = True, context = {'request': request})


        return Response({
            'hunt_template': serializer.data,
            'hunt_instances': hunt_instances_serializer.data,
            'riddle_items': riddle_items_serializer.data
        })
   
class RiddleItemList(generics.ListCreateAPIView):
    serializer_class = RiddleItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        scavenger_hunt = self.kwargs['hunt_template_id']
        return RiddleItem.objects.filter(scavenger_hunt = scavenger_hunt)
    
    def perform_create(self, serializer):
        scavenger_hunt = self.kwargs['hunt_template_id']
        serializer.save(scavenger_hunt = scavenger_hunt)

        