from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.transactions.models import Transaction
from apps.transactions.serializer import TransactionSerializer
from apps.wallets.models import Currency, Wallet
from apps.wallets.permissions import ReadOnlyAdminOrOwner, IsOwner
from apps.wallets.serializer import CurrencySerializer, WalletPublicSerializer, WalletSerializer, WalletUpdateSerializer
from django.db.models import Q

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (IsAdminUser(),)
    __basic_fields = ['name', 'code']
    filter_fields = __basic_fields
    search_fields = __basic_fields

    def get_permissions(self):
        if self.action == 'list':
            return (IsAuthenticated(),)
        return self.permission_classes


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletPublicSerializer
    permission_classes = [IsAuthenticated, ReadOnlyAdminOrOwner, ]
    __basic_fields = ['alias', 'balance']
    filter_fields = __basic_fields + ['owner', 'currency', ]
    search_fields = __basic_fields

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return WalletSerializer
        if self.action == 'update' or self.action == 'partial_update':
            return WalletUpdateSerializer

        if 'pk' in self.kwargs:
            wallet_id = int(self.kwargs['pk'])
            wallet = Wallet.objects.get(pk=wallet_id)
            if wallet.owner == self.request.user:
                return WalletSerializer

        if self.request.user.is_staff:
            return WalletSerializer

        return self.serializer_class

    @action(methods=['get'], detail=True)
    def transactions(self, request, pk=None):
        transactions = Transaction.objects.filter(Q(origin_id=pk) | Q(destination_id=pk))

        page = self.paginate_queryset(transactions)
        if page is not None:
            serializer = TransactionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def paginate_queryset(self, queryset):
        if self.paginator and (
                self.request.query_params.get('limit') == '' or self.request.query_params.get('limit', None) is None):
            return None
        return super().paginate_queryset(queryset)


class UserWalletsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated, IsOwner, ]
    __basic_fields = ['alias', 'balance']
    filter_fields = __basic_fields + ['currency']

    def get_queryset(self):
        if not self.request:
            return Wallet.objects.none()

        if self.request.query_params:
            queryset = self.filter_queryset(self.queryset)
            return queryset
        else:
            queryset = self.queryset
            return queryset

        return Wallet.objects.filter(owner_id=self.kwargs['pk'])

    def paginate_queryset(self, queryset):
        if self.paginator and (self.request.query_params.get('limit') == '' or self.request.query_params.get('limit', None) is None):
            return None
        return super().paginate_queryset(queryset)
