from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from myauth.views import UserViewSet
from softdesk.views import (
    ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet
)

# DefaultRouter includes a default API root view that returns a response
# containing hyperlinks to all the list views.
# https://www.django-rest-framework.org/api-guide/routers/#defaultrouter
router = routers.DefaultRouter()

router.register(
    prefix=r'users',
    viewset=UserViewSet,
    basename='user'
)
router.register(
    prefix=r'projects',
    viewset=ProjectViewSet,
    basename='project'
)

# To create a NestedDefaultRouter nested within a 'parent_router'
projects_router = routers.NestedDefaultRouter(
    parent_router=router,
    parent_prefix=r'projects',
    lookup='project'
)
projects_router.register(
    prefix=r'contributors',
    viewset=ContributorViewSet,
    basename='project-contributor'
)
projects_router.register(
    prefix=r'issues',
    viewset=IssueViewSet,
    basename='project-issue'
)

issues_router = routers.NestedDefaultRouter(
    parent_router=projects_router,
    parent_prefix='issues',
    lookup='issue'
)
issues_router.register(
    prefix=r'comments',
    viewset=CommentViewSet,
    basename='issue-comment'
)


urlpatterns = [
    path(
        route='admin/',
        view=admin.site.urls
    ),
    path(
        route='api-auth/v1/',
        view=include('rest_framework.urls')
    ),
    path(
        route='api/v1/token/',
        view=TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        route='api/v1/token/refresh/',
        view=TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    # the three following paths have the same route
    path(
        route='api/v1/',
        view=include(router.urls)
    ),
    path(
        route='api/v1/',
        view=include(projects_router.urls)
    ),
    path(
        route='api/v1/',
        view=include(issues_router.urls)
    ),
]
