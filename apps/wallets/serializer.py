from django.http import JsonResponse
from rest_framework import serializers

from apps.users.serializer import UserSerializer
from apps.wallets.models import Currency, Wallet
from commons.exceptions import ExceptionError


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'symbol', 'created_at', 'updated_at']


class WalletSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)
    currency_id = serializers.PrimaryKeyRelatedField(source='currency',  queryset=Currency.objects.all(), write_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'alias', 'created_at', 'updated_at', 'currency', 'currency_id', 'owner']
        extra_kwargs = {
            'balance': {'read_only': True},
        }

    def create(self, validated_data):
        wallet = Wallet(**validated_data)
        try:
            wallet.create()
            return wallet
        except ExceptionError as e:
            raise JsonResponse({e.key: e.message})

class WalletPublicSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = ('id', 'alias', 'created_at', 'updated_at', 'currency', 'owner')


class WalletUpdateSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'alias', 'created_at', 'updated_at', 'currency', 'owner']
        extra_kwargs = {
            'balance': {'read_only': True},
        }