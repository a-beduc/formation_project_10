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
        Check the current_project property and verify if the user is
        also the author of the project.
        Used for list view, where resource <pk> is not needed.
        """
        return view.current_project.author == request.user


class IsProjectContributor(BasePermission):
    """
    Permission for a Contributor of a Project.
    """
    def has_permission(self, request, view):
        """
        Check current_project_contributors_id property verify if the
        user is also a contributor of the project.
        Used for list view, where resource <pk> is not needed.
        """
        return request.user.id in view.current_project_contributors_id


class IsUserContributor(BasePermission):
    """
    Permission for a Contributor of a project to delete himself from
    the list of Contributors.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
