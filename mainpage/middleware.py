from django.utils.timezone import now


class SetLastVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.user.is_authenticated and request.user.profile.last_visit:
            if request.user.profile.last_visit.timestamp() < now().timestamp() - 15:
                request.user.profile.last_visit = now()
                request.user.profile.save(update_fields=["last_visit"])
        else:
            if request.user.is_authenticated:
                request.user.profile.last_visit = now()
                request.user.profile.save(update_fields=["last_visit"])
        response = self.get_response(request)
        return response
