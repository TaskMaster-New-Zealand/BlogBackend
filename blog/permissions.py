from rest_framework import permissions

class IsAuthenticatedForLikeDislike(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['toggle_like', 'toggle_dislike']:
            return request.user and request.user.is_authenticated
        return True