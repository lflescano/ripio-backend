from rest_framework.routers import DefaultRouter

from apps.transactions.api import TransactionViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')
urlpatterns = router.urls
