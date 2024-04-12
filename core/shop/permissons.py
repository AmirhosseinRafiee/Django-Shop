from django.http import Http404
from accounts.models import UserType

class IsAdminOrPublishedPermission:
    """
    Mixin to check if a user is admin or a product is published.
    """

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.has_permission(request, self.object):
            raise Http404("Page not found.")
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self, request, obj):
        if obj.is_published():
            return True
        if request.user.is_authenticated and request.user.type == UserType.admin.value:
            return True
        return False