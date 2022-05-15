from rest_framework import permissions
from .models import Route, Visit


class IsRouteOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.route.user

    def has_permission(self, request, view):
        if view.action == 'create':
            route = Route.objects.get(pk=request.data['route'])
            return request.user == route.user
        return True


class IsVisitOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.visit.route.user

    def has_permission(self, request, view):
        if view.action == 'create':
            visit = Visit.objects.get(pk=request.data['visit'])
            return request.user == visit.route.user
        return True
