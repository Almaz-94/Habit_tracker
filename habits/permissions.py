from rest_framework.permissions import BasePermission


class IsHabitCreator(BasePermission):
    """Check if current user is habit creator"""
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator
