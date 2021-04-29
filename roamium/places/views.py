from rest_framework import viewsets, permissions
from .models import Place
from .serializers import PlaceSerializer

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAdminUser()]

        return super(PlaceViewSet, self).get_permissions()
