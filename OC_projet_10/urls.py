from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from myauth.views import UserViewset
from softdesk.views import ProjectViewset, ContributorViewset, IssueViewset, CommentViewset


router = routers.SimpleRouter()

router.register('user', UserViewset, basename='user')
router.register('project', ProjectViewset, basename='project')
router.register('contributor', ContributorViewset, basename='contributor')
router.register('issue', IssueViewset, basename='issue')
router.register('comment', CommentViewset, basename='comment')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]
