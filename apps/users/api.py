from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User

from apps.users.permissions import IsAdminOrSameUser
from apps.users.serializer import UserSerializer, UserNoStaffSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSameUser, ]
    __basic_fields = ['username']
    filter_fields = __basic_fields + ['is_staff']
    search_fields = __basic_fields

    def get_serializer_class(self):
        if not self.request.user.is_staff:
            return UserNoStaffSerializer
        return self.serializer_class


class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)