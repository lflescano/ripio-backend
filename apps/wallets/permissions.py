from rest_framework import permissions

class ReadOnlyAdminOrOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user or request.user.is_staff

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'pk' in view.kwargs:
            return int(view.kwargs['pk']) == request.user.id
        return True