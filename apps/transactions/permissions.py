from rest_framework import permissions
from apps.wallets.models import Wallet


class AdminOrOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.origin.owner == request.user or obj.destination.owner == request.user or request.user.is_staff


class OwnerOrigin(permissions.BasePermission):

    def has_permission(self, request, view):
        if 'origin_id' not in request.data:
            return True

        wallet = Wallet.objects.get(pk=request.data['origin_id'])
        if wallet is None:
            return True

        return wallet.owner == request.user
