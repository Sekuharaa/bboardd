from django.urls import path, include
from .views import *

urlpatterns = [
   path('', AdList.as_view(), name='ad_list'),
   path('ad/<int:id>', AdDetail.as_view(), name='ad_detail'),
   path('ad/create/', AdCreate.as_view(), name='ad_create'),
   path('ad/<int:id>/edit/', AdEdit.as_view(), name='ad_edit'),
   path('<int:id>', CommentCreate.as_view(), name='comment_create'),
   path('comments/<int:id>/', AcceptedCommentList.as_view(), name='comment_list'),
   path('comment/<int:id>/delete/', CommentDelete.as_view(), name='comment_delete'),
   path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
   path('profile/', ProfileView.as_view(), name='profile'),
   path('comment/<int:id>/accept/', accept, name='accept')
]
