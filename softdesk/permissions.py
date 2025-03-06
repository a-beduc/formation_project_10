from softdesk.models import Contributor
from rest_framework.permissions import BasePermission


class IsProjectAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsProjectContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.contributors.filter(user=request.user).exists()


class ContributorIsProjectAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.project.author


class ContributorIsProjectContributor(BasePermission):
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        if not project_pk:
            return False
        return Contributor.objects.filter(project_id=project_pk, user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
