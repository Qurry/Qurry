from rest_framework import permissions


class IsOwner(permissions.DjangoObjectPermissions):
    # for view permission
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # for object level permissions
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.user.id == request.user.id
