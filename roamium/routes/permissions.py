from rest_framework.permissions import BasePermission
from .models import Route


class IsRouteOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.route.user

    def has_permission(self, request, view):
        if view.action == 'create':
            route = Route.objects.get(pk=request.data['route'])
            return request.user == route.user
        return True
