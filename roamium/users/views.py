from rest_framework import viewsets, permissions
from roamium.users.serializers import UserSerializer
from roamium.users.models import User
from roamium.users.permissions import IsSelfOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]

        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsSelfOrAdmin()]

        return super(UserViewSet, self).get_permissions()
