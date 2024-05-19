from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from .models import Profile, Participation, HuntInstance, ScavengerHunt,RiddleItem, RiddleItemSubmission, Item
from .serializers import UserSerializer, ProfileSerializer, ParticipationSerializer, HuntInstanceSerializer, ScavengerHuntSerializer, RiddleItemSerializer, RiddleItemSubmissionSerializer, ItemSerializer

# Create your views here.
# CreatUserView, LoginView, VerifyUserView

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        print('creating user...')
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        print(f"User created: {user}")
        refresh = RefreshToken.for_user(user)
        print(f"Generated tokens: Refresh - {refresh}, Access - {refresh.access_token}")
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

class RiddleItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RiddleItemSerializer
    queryset = RiddleItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
class RiddleItemSubmissionList(generics.ListCreateAPIView):
    serializer_class = RiddleItemSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        riddle_item = self.kwargs['riddle_item_id']
        participation = self.kwargs['participation_id']
        return RiddleItemSubmission.objects.filter(riddle_item = riddle_item, participation = participation)
    
    def perform_create(self, serializer):
        riddle_item = self.kwargs['riddle_item_id']
        participation = self.kwargs['participation_id']
        serializer.save(riddle_item = riddle_item, participation = participation)

class RiddleItemSubmissionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RiddleItemSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context = {'request': request})
        
        riddle_item_id = self.kwargs['riddle_item_id']
        riddle_item = RiddleItem.objects.get(id = riddle_item_id)
        riddle_item_serializer = RiddleItemSerializer(riddle_item, context = {'request': request})

        participation_id = self.kwargs['participation_id']
        participation = Participation.objects.get(id = participation_id)
        participation_serializer = ParticipationSerializer(participation, context = {'request': request})

        return Response({
            'riddle_item_submission': serializer.data,
            'riddle_item': riddle_item_serializer.data,
            'participation': participation_serializer.data
        })
    
class ItemList(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            # If the request data is a list, we need to validate and save each item
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Handle single dictionary case
            return super().create(request, *args, **kwargs)

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

