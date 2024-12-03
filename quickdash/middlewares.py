from django.conf import settings
from django.http import HttpResponse
import os

class ServeMediaFileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path.startswith(settings.MEDIA_URL):
            file_path = os.path.join(settings.MEDIA_ROOT, request.path[len(settings.MEDIA_URL):])
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    return HttpResponse(f.read(), content_type='application/octet-stream')
        return self.get_response(request)