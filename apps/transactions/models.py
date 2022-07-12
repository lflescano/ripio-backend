from django.db import models, transaction
from apps.wallets.models import Wallet
from commons.base_model import BaseModel
from commons.exceptions import ExceptionError


class Transaction(BaseModel):
    amount = models.DecimalField(max_digits = 12,
                         decimal_places = 2)

    origin = models.ForeignKey('wallets.Wallet', related_name='+', on_delete=models.PROTECT, )
    destination = models.ForeignKey('wallets.Wallet', related_name='+', on_delete=models.PROTECT)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        with transaction.atomic():
            Wallet.objects.select_for_update(nowait=True).filter(pk__in=[self.origin.id, self.destination.id])

            self.amount = abs(self.amount)
            if self.origin.currency.id != self.destination.currency.id:
                raise ExceptionError('error',
                                'El origen y el destino de la transacción deben tener la misma moneda.')
            if not self.origin.check_balance(self.amount):
                raise ExceptionError('error',
                                'No cuenta con el balance necesario para realizar la transacción.')

            self.origin.subtract_money(self.amount)
            self.destination.add_money(self.amount)
            return super(Transaction, self).save(*args, **kwargs)