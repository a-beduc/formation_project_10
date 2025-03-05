from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from myauth.views import UserViewset
from softdesk.views import ProjectViewset, ContributorViewset, IssueViewset, CommentViewset


router = routers.DefaultRouter()

router.register(r'users', UserViewset, basename='user')
router.register(r'projects', ProjectViewset, basename='project')

projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'contributors', ContributorViewset, basename='project-contributor')
projects_router.register(r'issues', IssueViewset, basename='project-issue')

issues_router = routers.NestedDefaultRouter(projects_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewset, basename='issue-comment')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/v1/', include('rest_framework.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(projects_router.urls)),
    path('api/v1/', include(issues_router.urls)),
]
