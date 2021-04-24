from rest_framework import permissions

class IsSelfOrAdmin(permissions.BasePermission):
    message = 'Non-admin users can only apply this action to themselves.'

    def has_object_permission(self, request, view, obj):
        return request.user.pk == obj.pk or request.user.has_perm(permissions.IsAdminUser)
