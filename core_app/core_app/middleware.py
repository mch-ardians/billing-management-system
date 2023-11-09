from django.urls import reverse
from django.http import HttpResponseRedirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path != reverse('authenticate:login'):
            return HttpResponseRedirect(reverse('authenticate:login'))
        response = self.get_response(request)
        return response