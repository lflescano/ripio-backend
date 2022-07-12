from django.test import TestCase

from apps.transactions.models import Transaction
from apps.wallets.models import Currency, Wallet
from django.contrib.auth.models import User

from commons.exceptions import ExceptionError


class TestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="prueba1", email="prueba1@gmail.com")
        user2 = User.objects.create(username="prueba2", email="prueba2@gmail.com")
        currency1 = Currency.objects.create(code=1, name="moneda1", symbol="1")
        currency2 = Currency.objects.create(code=2, name="moneda2", symbol="2")
        wallet1 = self._fill_wallet('user1-wallet1', user1, currency1, 500)
        wallet2 = self._fill_wallet('user1-wallet2', user1, currency2, 500)
        wallet3 = self._fill_wallet('user2-wallet1', user2, currency1, 500)
        wallet4 = self._fill_wallet('user2-wallet2', user2, currency2, 500)

    def test_default_transaction(self):
        transaction = Transaction()
        transaction.amount = 200
        transaction.origin = Wallet.objects.get(alias="user1-wallet1")
        transaction.destination = Wallet.objects.get(alias="user2-wallet1")
        try:
            transaction.save()
            self.assertEqual(transaction.origin.balance, 300)
            self.assertEqual(transaction.destination.balance, 700)
        except ExceptionError as e:
            self.fail("No se pudo realizar la transaccion")

    def test_transaction_different_coins(self):
        transaction = Transaction()
        transaction.amount = 200
        transaction.origin = Wallet.objects.get(alias="user1-wallet1")
        transaction.destination = Wallet.objects.get(alias="user2-wallet2")
        try:
            transaction.save()
            self.fail("Se pudo realizar la transaccion de todas formas")
        except ExceptionError as e:
            pass

    def test_transaction_without_enough_money(self):
        transaction = Transaction()
        transaction.amount = 600
        transaction.origin = Wallet.objects.get(alias="user1-wallet1")
        transaction.destination = Wallet.objects.get(alias="user2-wallet2")
        try:
            transaction.save()
            self.fail("Se pudo realizar la transaccion de todas formas")
        except ExceptionError as e:
            pass

    def _fill_wallet(self, alias, user, currency, balance):
        wallet = Wallet()
        wallet.alias = alias
        wallet.owner = user
        wallet.currency = currency
        wallet.balance = balance
        wallet.create()
        return wallet
