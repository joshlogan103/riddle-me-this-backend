from rest_framework import serializers
from .models import Profile, ScavengerHunt, HuntInstance, Item, RiddleItem, RiddleItemSubmission, Participation
from django.contrib.auth.models import User
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
class ScavengerHuntSerializer(serializers.ModelSerializer):
    riddle_items = serializers.SerializerMethodField()
    hunt_instances = serializers.SerializerMethodField()
    class Meta:
        model = ScavengerHunt
        fields = "__all__"
        read_only_fields = ('creator',)
    def get_riddle_items(self, obj):
        return RiddleItemSerializer(obj.riddleitem_set.all(), many=True).data
    def get_hunt_instances(self, obj):
        return HuntInstanceSerializer(obj.huntinstance_set.all(), many=True).data
class RiddleItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    scavenger_hunt = ScavengerHuntSerializer(read_only=True)
    riddle_item_submissions = serializers.SerializerMethodField()
    class Meta:
        model = RiddleItem
        fields = "__all__"
    def get_riddle_item_submissions(self, obj):
        return RiddleItemSubmissionSerializer(obj.riddleitemsubmission_set.all(), many=True).data
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
    riddle_item = RiddleItemSerializer(read_only=True)
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
class HuntInstanceSerializer(serializers.ModelSerializer):
    scavenger_hunt = ScavengerHuntSerializer(read_only=True)
    participations = ParticipationSerializer(many=True, read_only=True)
    class Meta:
        model = HuntInstance
        fields = "__all__"
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    hunt_instances = HuntInstanceSerializer(many=True, read_only=True)
    participations = ParticipationSerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = "__all__"
