from snowebsvg import settings


def clean_middleware(value):
    if len(value) > 10:
        return ValueError
    if value == 'none':
        value = ''
    return value


conf = (
    ('theme', settings.SVG_DEFAULT_THEME),
    ('variant', settings.SVG_DEFAULT_VARIANT),
)


class SettingsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'settings' not in request.session:
            request.session['settings'] = {}

        for conf_key, conf_default in conf:
            if conf_key not in request.session:
                request.session[conf_key] = conf_default
            if conf_key in request.GET:
                try:
                    value = clean_middleware(request.GET[conf_key])
                    request.session[conf_key] = value
                except ValueError:
                    pass
        return self.get_response(request)
