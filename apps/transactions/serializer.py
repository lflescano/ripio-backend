from rest_framework import serializers
from apps.transactions.models import Transaction
from apps.wallets.models import Wallet
from apps.wallets.serializer import WalletPublicSerializer
from commons.exceptions import ExceptionError


class TransactionSerializer(serializers.ModelSerializer):
    origin = WalletPublicSerializer(read_only=True)
    origin_id = serializers.PrimaryKeyRelatedField(source='origin', queryset=Wallet.objects.all(), write_only=True)
    destination = WalletPublicSerializer(read_only=True)
    destination_id = serializers.PrimaryKeyRelatedField(source='destination', queryset=Wallet.objects.all(),
                                                        write_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'created_at', 'origin', 'origin_id', 'destination', 'destination_id']

    def create(self, validated_data):
        transaction = Transaction(**validated_data)
        try:
            transaction.save()
            return transaction
        except ExceptionError as e:
            raise serializers.ValidationError({e.key: e.message})
