from django.test import TestCase

from apps.wallets.models import Currency, Wallet
from django.contrib.auth.models import User

from commons.exceptions import ExceptionError


class TestCase(TestCase):
    def setUp(self):
        User.objects.create(username="lflescano", email="lflescano@gmail.com")
        Currency.objects.create(code='USD', name="DOLLAR", symbol="$")

    def test_default_wallet_create(self):
        wallet = self._fill_wallet('Wallet', 'lflescano', 'USD')
        try:
            wallet.create()
            pass
        except ExceptionError as e:
            self.fail("No se pudo crear la billetera")

    def test_error_wallet_create(self):
        wallet = self._fill_wallet('Wallet', 'lflescano', 'USD')
        another_wallet = self._fill_wallet('AnotherWallet', 'lflescano', 'USD')
        try:
            wallet.create()
            another_wallet.create()
            self.fail("Se crearon las 2 billeteras")
        except ExceptionError as e:
            self.assertIs(wallet.id is not None, True)

    def test_currency_create(self):
        try:
            Currency.objects.create(code='ARS', name="Peso", symbol="$")
        except ExceptionError as e:
            self.fail("No se pudo crear moneda")

    def _fill_wallet(self, alias, username, code):
        wallet = Wallet()
        wallet.alias = alias
        wallet.owner = User.objects.get(username=username)
        wallet.currency = Currency.objects.get(code=code)
        return wallet
