import os
from binascii import hexlify

from django.db import models

from commons.base_model import BaseModel
from commons.exceptions import ExceptionError


def create_hash():
    return hexlify(os.urandom(5))


class Currency(BaseModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Wallet(BaseModel):
    balance = models.DecimalField(max_digits = 12,
                         decimal_places = 2,
                         default=0)
    alias = models.CharField(max_length=25, default=create_hash)
    currency = models.ForeignKey('Currency', related_name='wallets', on_delete=models.PROTECT, )
    owner = models.ForeignKey('auth.User', related_name='wallets', on_delete=models.PROTECT)

    def __str__(self):
        return self.owner.username + " - " + self.alias + " - (" + self.currency.name + ")"

    def add_money(self, amount):
        self.balance += amount
        return self.save()

    def subtract_money(self, amount):
        self.balance -= amount
        return self.save()

    def check_balance(self, amount):
        return self.balance >= amount

    def create(self):
        if Wallet.objects.filter(owner_id=self.owner.id, currency_id=self.currency.id).count() > 0:
            raise ExceptionError('currency', 'El usuario ya tiene una billetera con esta moneda.')
        return self.save()

    class Meta:
        ordering = ['created_at']
