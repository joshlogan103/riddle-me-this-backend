from rest_framework import serializers
from .models import Profile, ScavengerHunt, HuntInstance, Item, RiddleItem, RiddleItemSubmission, Participation
from django.contrib.auth.models import User

# Simple Serializers

class SimpleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class SimpleScavengerHuntSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScavengerHunt
        fields = "__all__"
        read_only_fields = ('creator',)

class SimpleRiddleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiddleItem
        fields = "__all__"

class SimpleRiddleItemSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiddleItemSubmission
        fields = "__all__"

class SimpleParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = "__all__"

class SimpleHuntInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntInstance
        fields = "__all__"

class SimpleProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

# Full Serializers

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class ScavengerHuntSerializer(serializers.ModelSerializer):
    riddle_items = SimpleRiddleItemSerializer(many=True, read_only=True)
    hunt_instances = SimpleHuntInstanceSerializer(many=True, read_only=True)

    class Meta:
        model = ScavengerHunt
        fields = "__all__"
        read_only_fields = ('creator',)

class RiddleItemSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    item = SimpleItemSerializer(read_only=True)
    scavenger_hunt = SimpleScavengerHuntSerializer(read_only=True)
    riddle_item_submissions = SimpleRiddleItemSubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = RiddleItem
        fields = "__all__"


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

class RiddleItemSubmissionSerializer(serializers.ModelSerializer):
    riddle_item = SimpleRiddleItemSerializer(read_only=True)
    participation = SimpleParticipationSerializer(read_only=True)

    class Meta:
        model = RiddleItemSubmission
        fields = "__all__"

class ParticipationSerializer(serializers.ModelSerializer):
    profile = SimpleProfileSerializer(read_only=True)
    hunt_instance = SimpleHuntInstanceSerializer(read_only=True)
    riddle_item_submissions = SimpleRiddleItemSubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = Participation
        fields = "__all__"

class HuntInstanceSerializer(serializers.ModelSerializer):
    scavenger_hunt = SimpleScavengerHuntSerializer(read_only=True)
    participations = SimpleParticipationSerializer(many=True, read_only=True)

    class Meta:
        model = HuntInstance
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    hunt_instances = SimpleHuntInstanceSerializer(many=True, read_only=True)
    participations = SimpleParticipationSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
