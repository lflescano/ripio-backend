from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.transactions.permissions import AdminOrOwner, OwnerOrigin
from apps.transactions.models import Transaction
from apps.transactions.serializer import TransactionSerializer


class TransactionViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser()]
    filter_fields = ['amount', 'origin', 'destination']

    def get_permissions(self):
        if self.action == 'create':
            return IsAuthenticated(), OwnerOrigin(),
        elif self.action == 'retrieve':
            return IsAuthenticated(), AdminOrOwner(),
        return self.permission_classes
