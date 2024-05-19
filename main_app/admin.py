from django.contrib import admin
from .models import Profile, ScavengerHunt, HuntInstance, Item, RiddleItem, Participation, RiddleItemSubmission

# Register your models here.
admin.site.register(ScavengerHunt)
admin.site.register(HuntInstance)
admin.site.register(Item)
admin.site.register(RiddleItem)
admin.site.register(Profile)
admin.site.register(Participation)
admin.site.register(RiddleItemSubmission)