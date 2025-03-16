from softdesk.models import Contributor, Project
from rest_framework.permissions import BasePermission


class IsResourceAuthor(BasePermission):
    """
    Permission for the Author of a Resource (used for Issue & Comment).
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsProjectAuthor(BasePermission):
    """
    Permission for the Author of a Project.
    """
    def has_permission(self, request, view):
        """
        Check the dict found in view.kwargs to get the project ID and with a query verify if the user is also the
        author of the project.
        Used for list view, where resource <pk> is not needed.
        """
        if 'project_pk' in view.kwargs.keys():
            project_pk = view.kwargs.get('project_pk')
        else:
            project_pk = view.kwargs.get('pk')
        if not project_pk:
            return False
        project = Project.objects.get(pk=project_pk)
        return project.author == request.user

    def has_object_permission(self, request, view, obj):
        """
        Check the dict found in view.kwargs to get the project ID and with a query verify if the user is also the
        author of the project.
        Used in detail view, where resource <pk> is needed.
        """
        if 'project_pk' in view.kwargs.keys():
            project_pk = view.kwargs.get('project_pk')
        else:
            project_pk = view.kwargs.get('pk')
        if not project_pk:
            return False
        project = Project.objects.get(pk=project_pk)
        return project.author == request.user


class IsProjectContributor(BasePermission):
    """
    Permission for a Contributor of a Project.
    """
    def has_permission(self, request, view):
        """
        Check the dict found in view.kwargs to get the project ID and with a query verify if the user is also the
        author of the project.
        Used for list view, where resource <pk> is not needed.
        """
        if 'project_pk' in view.kwargs.keys():
            project_pk = view.kwargs.get('project_pk')
        else:
            project_pk = view.kwargs.get('pk')
        if not project_pk:
            return False
        return Contributor.objects.filter(project_id=project_pk, user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        """
        Check the dict found in view.kwargs to get the project ID and with a query verify if the user is also the
        author of the project.
        Used in detail view, where resource <pk> is needed.
        """
        if 'project_pk' in view.kwargs.keys():
            project_pk = view.kwargs.get('project_pk')
        else:
            project_pk = view.kwargs.get('pk')
        if not project_pk:
            return False
        return Contributor.objects.filter(project_id=project_pk, user=request.user).exists()


class IsUserContributor(BasePermission):
    """
    Permission for a Contributor of a project to delete himself from the list of Contributors.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
