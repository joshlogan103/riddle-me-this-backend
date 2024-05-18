from django.urls import path
from .views import (
    CreateUserView,
    LoginView,
    VerifyUserView,
    ProfileList,
    ProfileDetail,
    ParticipationsList,
    ParticipationDetail,
    HuntInstanceList,
    HuntInstanceDetail,
    HuntTemplateList,
    HuntTemplateDetail,
    RiddleItemList,
    RiddleItemDetail,
    ItemList,
    ItemDetail,
    RiddleItemSubmissionList,
    RiddleItemSubmissionDetail
)

urlpatterns = [
    # Users
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),

    # Profiles
    path('users/<int:user_id>/profiles/', ProfileList.as_view(), name='profile-list'),
    path('users/<int:user_id>/profiles/<int:id>/', ProfileDetail.as_view(), name='profile-detail'),

    # Participations
    path('profiles/<int:profile_id>/participations/', ParticipationsList.as_view(), name='participations-list'),
    path('profiles/<int:profile_id>/participations/<int:participation_id>/', ParticipationDetail.as_view(), name='participation-detail'),

    # Hunt Instances
    path('hunt-templates/<int:hunt_template_id>/hunt-instances/', HuntInstanceList.as_view(), name='hunt-instance-list'),
    path('hunt-templates/<int:hunt_template_id>/hunt-instances/<int:hunt_instance_id>/', HuntInstanceDetail.as_view(), name='hunt-instance-detail'),

    # Hunt Templates
    path('hunt-templates/', HuntTemplateList.as_view(), name='hunt-template-list'),
    path('hunt-templates/<int:hunt_template_id>/', HuntTemplateDetail.as_view(), name='hunt-template-detail'),

    # Riddle Items
    path('hunt-templates/<int:hunt_template_id>/riddle-items/', RiddleItemList.as_view(), name='riddle-item-list'),
    path('hunt-templates/<int:hunt_template_id>/riddle-items/<int:riddle_item_id>/', RiddleItemDetail.as_view(), name='riddle-item-detail'),

    # Riddle Item Submissions
    path('hunt-templates/<int:hunt_template_id>/riddle-items/<int:riddle_item_id>/participations/<int:participation_id>/riddle-item-submissions/', RiddleItemSubmissionList.as_view(), name='riddle-item-submission-list'),
    path('hunt-templates/<int:hunt_template_id>/riddle-items/<int:riddle_item_id>/participations/<int:participation_id>/riddle-item-submissions/<int:riddle_item_submission_id>/', RiddleItemSubmissionDetail.as_view(), name='riddle-item-submission-detail'),

    # Items
    path('items/', ItemList.as_view(), name='item-list'),
    path('items/<int:id>/', ItemDetail.as_view(), name='item-detail'),
]