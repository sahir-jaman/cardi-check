from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from django_filters.rest_framework import DjangoFilterBackend

from ..serializers.users import PrivateUserListSerializer

User = get_user_model()


class PrivateUserList(ListAPIView):
    queryset = User.objects.filter()
    serializer_class = PrivateUserListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = ["type"]
    pagination_class = None
