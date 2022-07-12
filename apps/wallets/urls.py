from rest_framework.routers import DefaultRouter

from apps.wallets.api import CurrencyViewSet, WalletViewSet, UserWalletsViewSet

router = DefaultRouter()
router.register(r'currencies', CurrencyViewSet, basename='currency')
router.register(r'wallets', WalletViewSet, basename='wallets')
router.register(r'users/(?P<pk>[0-9]+)/wallets', UserWalletsViewSet, basename='user_wallets')
urlpatterns = router.urls
