from softdesk.models import Contributor, Project
from rest_framework.permissions import BasePermission


class IsResourceAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsProjectAuthor(BasePermission):
    def has_permission(self, request, view):
        if 'project_pk' in view.kwargs.keys():
            project_pk = view.kwargs.get('project_pk')
        else:
            project_pk = view.kwargs.get('pk')
        if not project_pk:
            return False
        project = Project.objects.get(pk=project_pk)
        return project.author == request.user

    def has_object_permission(self, request, view, obj):
        if 'project_pk' in view.kwargs.keys():
            project_pk = view.kwargs.get('project_pk')
        else:
            project_pk = view.kwargs.get('pk')
        if not project_pk:
            return False
        project = Project.objects.get(pk=project_pk)
        return project.author == request.user


class IsProjectContributor(BasePermission):
    def has_permission(self, request, view):
        if 'project_pk' in view.kwargs.keys():
            project_pk = view.kwargs.get('project_pk')
        else:
            project_pk = view.kwargs.get('pk')
        if not project_pk:
            return False
        return Contributor.objects.filter(project_id=project_pk, user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if 'project_pk' in view.kwargs.keys():
            project_pk = view.kwargs.get('project_pk')
        else:
            project_pk = view.kwargs.get('pk')
        if not project_pk:
            return False
        return Contributor.objects.filter(project_id=project_pk, user=request.user).exists()


class IsUserContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
