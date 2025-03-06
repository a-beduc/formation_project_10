from rest_framework.permissions import BasePermission


class IsProjectAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsProjectContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.contributors.filter(user=request.user).exists()
