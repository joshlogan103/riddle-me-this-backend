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

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class ScavengerHuntSerializer(serializers.ModelSerializer):
    riddle_items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    hunt_instances = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = ScavengerHunt
        fields = "__all__"
        read_only_fields = ('creator',)

class HuntInstanceSerializer(serializers.ModelSerializer):
    scavenger_hunt = serializers.PrimaryKeyRelatedField(read_only=True)
    participations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = HuntInstance
        fields = "__all__"

class RiddleItemSubmissionSerializer(serializers.ModelSerializer):
    riddle_item = serializers.PrimaryKeyRelatedField(read_only=True)
    participation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RiddleItemSubmission
        fields = "__all__"

class ParticipationSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    hunt_instance = serializers.PrimaryKeyRelatedField(read_only=True)
    riddle_item_submissions = RiddleItemSubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = Participation
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    hunt_instances = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    participations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"

class RiddleItemSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    scavenger_hunt = serializers.PrimaryKeyRelatedField(read_only=True)
    riddle_item_submissions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = RiddleItem
        fields = "__all__"
