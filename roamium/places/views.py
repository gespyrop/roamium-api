from rest_framework import viewsets, permissions
from .models import Place
from .serializers import PlaceSerializer

class PlaceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.IsAuthenticated()]

        return super(PlaceViewSet, self).get_permissions()
