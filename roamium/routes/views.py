from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Route, Visit
from .serializers import RouteSerializer, VisitSerializer
from .permissions import IsRouteOwner


class RouteViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        # List only finished routes
        self.queryset = self.queryset.filter(finished=True)
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['POST'])
    def complete(self, request, pk=None):
        '''Complete a route'''
        route = self.get_object()

        # Delete empty routes
        if route.visit_set.count() == 0:
            route.delete()
            return Response(
                {'message': 'Deleted empty route.'},
                status=status.HTTP_204_NO_CONTENT
            )

        # Complete non-empty routes
        route.finished = True
        route.save()

        return Response(
            self.get_serializer(route).data,
            status=status.HTTP_200_OK
        )


class VisitViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsRouteOwner)
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

    def get_queryset(self):
        return self.queryset.filter(route__user=self.request.user)
