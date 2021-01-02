class ThemeMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'theme' in request.GET:
            request.session['theme'] = request.GET['theme']
        return self.get_response(request)
