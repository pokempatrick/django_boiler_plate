from rest_framework import permissions


class IsAuthenficatedOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        return bool(request.user and request.user.is_authenticated)


class IsArticleOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True

        return request.user == obj.added_by
