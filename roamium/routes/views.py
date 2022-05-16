from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import PLACE_SOURCES, Route, Visit, Review
from .serializers import RouteSerializer, VisitSerializer, ReviewSerializer
from .permissions import IsRouteOwner, IsVisitOwner


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

    @action(detail=True, methods=['GET'])
    def review(self, request, pk=None):
        try:
            return Response(ReviewSerializer(self.get_object().review).data)
        except Review.DoesNotExist:
            return Response(
                {'detail': 'Review not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


ACCEPTED_PLACE_SOURCES = list(map(lambda source: source[0], PLACE_SOURCES))


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsVisitOwner)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(visit__route__user=self.request.user)
        return self.queryset

    @action(detail=False, methods=['GET'])
    def place(self, request):
        # Get the place source form query parameters
        source = str(request.query_params.get('source'))

        # Validate source
        if not source:
            return Response(
                {'message': "String parameter 'source' is required."},
                status.HTTP_400_BAD_REQUEST
            )

        if source not in ACCEPTED_PLACE_SOURCES:
            joined_values = ','.join(ACCEPTED_PLACE_SOURCES)
            message = f"'{source}' is not in ({joined_values})."

            return Response(
                {'message': message},
                status.HTTP_400_BAD_REQUEST
            )

        # Get the place id from query parameters
        try:
            place_id = int(request.query_params.get('place_id'))
        except ValueError:
            return Response(
                {'message': "Parameter 'place_id' must be an integer."},
                status.HTTP_400_BAD_REQUEST
            )
        except TypeError:
            return Response(
                {'message': "Parameter 'place_id' is required."},
                status.HTTP_400_BAD_REQUEST
            )

        # Get the place's reviews
        reviews = Review.objects.filter(
            visit__place_source=source,
            visit__place_id=place_id
        )

        return Response(ReviewSerializer(reviews, many=True).data)
