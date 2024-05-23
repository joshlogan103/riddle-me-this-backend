from django.urls import path
from .views import CreateUserView, LoginView, VerifyUserView, ProfileList, ProfileDetail, ParticipationListByProfile, ParticipationListByHuntInstance, ParticipationListByHuntInstanceAndProfile, ParticipationCreate, ParticipationDetail, HuntInstanceListAll, HuntInstanceList, HuntInstanceDetail, HuntTemplateList, HuntTemplateDetail, RiddleItemList, RiddleItemDetail, RiddleItemSubmissionList, RiddleItemSubmissionDetail, ItemList, ItemDetail, APILandingPage, upload_image 


urlpatterns = [
    # API Landing Page
    path('', APILandingPage.as_view(), name='api-landing-page'),

    # Users
    path('api/users/register/', CreateUserView.as_view(), name='register'),
    path('api/users/login/', LoginView.as_view(), name='login'),
    path('api/users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),

    # Profiles
    path('api/profiles/', ProfileList.as_view(), name='profile-list'),
    path('api/users/<int:user_id>/profiles/detail/', ProfileDetail.as_view(), name='profile-detail'),

    # Participations
    path('api/profiles/<int:profile_id>/participations/', ParticipationListByProfile.as_view(), name='participations-list-by-profile'),
    path('api/hunt-instance/<int:hunt_instance_id>/participations/', ParticipationListByHuntInstance.as_view(), name='participations-list-by-hunt-instance'),
    path('api/profiles/<int:profile_id>/hunt-instance/<int:hunt_instance_id>/participations/', ParticipationListByHuntInstanceAndProfile.as_view(), name='participations-list-by-profile-and-hunt-instance'),
    path('api/profiles/<int:profile_id>/hunt-instance/<int:hunt_instance_id>/participations/', ParticipationCreate.as_view(), name = 'participation-create'),
    path('api/profiles/<int:profile_id>/hunt-instance/<int:hunt_instance_id>/participations/<int:id>/', ParticipationDetail.as_view(), name='participation-detail'),

    # Hunt Instances
    path('api/hunt-instances/', HuntInstanceListAll.as_view(), name='hunt-instance-list-all'),
    path('api/hunt-templates/<int:hunt_template_id>/hunt-instances/', HuntInstanceList.as_view(), name='hunt-instance-list'),
    path('api/hunt-templates/<int:hunt_template_id>/hunt-instances/<int:id>/', HuntInstanceDetail.as_view(), name='hunt-instance-detail'),

    # Hunt Templates
    path('api/hunt-templates/', HuntTemplateList.as_view(), name='hunt-template-list'),
    path('api/hunt-templates/<int:id>/', HuntTemplateDetail.as_view(), name='hunt-template-detail'),

    # Riddle Items
    path('api/hunt-templates/<int:hunt_template_id>/riddle-items/', RiddleItemList.as_view(), name='riddle-item-list'),
    path('api/hunt-templates/<int:hunt_template_id>/riddle-items/<int:id>/', RiddleItemDetail.as_view(), name='riddle-item-detail'),

    # Riddle Item Submissions
    path('api/hunt-templates/<int:hunt_template_id>/riddle-items/<int:riddle_item_id>/participations/<int:participation_id>/riddle-item-submissions/', RiddleItemSubmissionList.as_view(), name='riddle-item-submission-list'),
    path('api/hunt-templates/<int:hunt_template_id>/riddle-items/<int:riddle_item_id>/participations/<int:participation_id>/riddle-item-submissions/<int:id>/', RiddleItemSubmissionDetail.as_view(), name='riddle-item-submission-detail'),

    # Items
    path('api/items/', ItemList.as_view(), name='item-list'),
    path('api/items/<int:id>/', ItemDetail.as_view(), name='item-detail'),
    
    # TESTING
    path('api/upload/', upload_image, name='upload_image'),
]