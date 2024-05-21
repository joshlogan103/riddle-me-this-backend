from django.db import models
from django.contrib.auth.models import User

DIFFICULTY = (
    ('E', 'Easy'),
    ('M', 'Medium'),
    ('H', 'Hard'),
)

class ScavengerHunt(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(
        max_length=1,
        choices=DIFFICULTY,
        default=DIFFICULTY[0][0]
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class HuntInstance(models.Model):
    scavenger_hunt = models.ForeignKey(ScavengerHunt, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.scavenger_hunt.name} - {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}"


class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} in {self.category}" 


class RiddleItem(models.Model):
    riddle = models.CharField(max_length=100)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    scavenger_hunt = models.ForeignKey(ScavengerHunt, on_delete=models.CASCADE)

    def __str__(self):
        return self.riddle


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.URLField()
    hunt_instances = models.ManyToManyField(HuntInstance, through='Participation')

    def __str__(self):
        return self.user.username


class Participation(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    hunt_instance = models.ForeignKey(HuntInstance, on_delete=models.CASCADE)
    place_finished = models.IntegerField()
    items_found = models.IntegerField()
    time_of_last_item_found = models.DateTimeField()

    def __str__(self):
        return f"{self.profile.user.username} - {self.hunt_instance.scavenger_hunt.name}"


class RiddleItemSubmission(models.Model):
    riddle_item = models.ForeignKey(RiddleItem, on_delete=models.CASCADE)
    participation = models.ForeignKey(Participation, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.riddle_item.riddle} - {self.participation.profile.user.username} - correct: {self.correct}"