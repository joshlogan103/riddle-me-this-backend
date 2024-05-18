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

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
        extra_kwargs = {'url': {'view_name': 'item-detail', 'lookup_field': 'id'}}

class ScavengerHuntSerializer(serializers.HyperlinkedModelSerializer):
    riddle_items = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='riddleitem-detail')
    hunt_instances = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='huntinstance-detail')

    class Meta:
        model = ScavengerHunt
        fields = "__all__"
        extra_kwargs = {'url': {'view_name': 'scavenger-hunt-detail', 'lookup_field': 'id'}}

class HuntInstanceSerializer(serializers.HyperlinkedModelSerializer):
    scavenger_hunt = serializers.HyperlinkedRelatedField(read_only=True, view_name='scavengerhunt-detail')
    participations = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='participation-detail')

    class Meta:
        model = HuntInstance
        fields = "__all__"
        extra_kwargs = {'url': {'view_name': 'hunt-instance-detail', 'lookup_field': 'id'}}

class RiddleItemSubmissionSerializer(serializers.HyperlinkedModelSerializer):
    riddle_item = serializers.HyperlinkedRelatedField(read_only=True, view_name='riddleitem-detail')
    participation = serializers.HyperlinkedRelatedField(read_only=True, view_name='participation-detail')

    class Meta:
        model = RiddleItemSubmission
        fields = "__all__"
        extra_kwargs = {'url': {'view_name': 'riddle-item-submission-detail', 'lookup_field': 'id'}}

class ParticipationSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.HyperlinkedRelatedField(view_name='profile-detail', read_only=True, lookup_field='id')
    hunt_instance = serializers.HyperlinkedRelatedField(view_name='huntinstance-detail', read_only=True, lookup_field='id')
    riddle_item_submissions = RiddleItemSubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = Participation
        fields = "__all__"
        extra_kwargs = {'url': {'view_name': 'participation-detail', 'lookup_field': 'id'}}

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    hunt_instances = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='huntinstance-detail')
    participations = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='participation-detail')

    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {'url': {'view_name': 'profile-detail', 'lookup_field': 'id'}}

class RiddleItemSerializer(serializers.HyperlinkedModelSerializer):
    item = ItemSerializer(read_only=True)
    scavenger_hunt = serializers.HyperlinkedRelatedField(read_only=True, view_name='scavengerhunt-detail')
    riddle_item_submissions = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='riddleitemsubmission-detail')

    class Meta:
        model = RiddleItem
        fields = "__all__"
        extra_kwargs = {'url': {'view_name': 'riddle-item-detail', 'lookup_field': 'id'}}
