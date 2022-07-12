from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.users.api import UserViewSet, CurrentUserView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
urlpatterns = [
    re_path(r'^users/current', CurrentUserView.as_view()),
]
urlpatterns += router.urls
