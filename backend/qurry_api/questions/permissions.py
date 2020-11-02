from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class CanEdit(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and not request.user.is_authenticated():
            return True
        elif not request.user.is_authenticated() and request.method != "POST":
            return False
        elif request.method in permissions.SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated():
            return False
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.username == request.user.username