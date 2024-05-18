from rest_framework import serializers
from .models import Profile, ScavengerHunt, HuntInstance, Item, RiddleItem, RiddleItemSubmission, Participation
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user

class ScavengerHuntSerializer(serializers.HyperlinkedModelSerializer):
    riddle_items = RiddleItemSerializer(many=True, read_only=True)
    hunt_instances = HuntInstanceSerializer(many=True, read_only=True)

    class Meta:
        model = ScavengerHunt
        fields = "__all__"
        extra_kwargs = {'url': {'view_name': 'scavenger-hunt-detail', 'lookup_field': 'id'}}

class HuntInstanceSerializer(serializers.HyperlinkedModelSerializer):
    scavenger_hunt = ScavengerHuntSerializer(read_only=True)
    participations = ParticipationSerializer(many=True, read_only=True)

    class Meta:
        model = HuntInstance
        fields = "__all__"
        extra_kwargs = {'url': {'view_name': 'hunt-instance-detail', 'lookup_field': 'id'}}