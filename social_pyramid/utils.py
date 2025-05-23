import warnings
from functools import wraps

from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound
from pyramid.threadlocal import get_current_registry
from social_core.backends.utils import get_backend, user_backends_data
from social_core.utils import get_strategy, module_member, setting_name

DEFAULTS = {
    "STORAGE": "social_pyramid.models.PyramidStorage",
    "STRATEGY": "social_pyramid.strategy.PyramidStrategy",
}


def get_helper(name):
    settings = get_current_registry().settings
    return settings.get(setting_name(name), DEFAULTS.get(name))


def load_strategy(request):
    return get_strategy(get_helper("STRATEGY"), get_helper("STORAGE"), request)


def load_backend(strategy, name, redirect_uri):
    backends = get_helper("AUTHENTICATION_BACKENDS")
    Backend = get_backend(backends, name)
    return Backend(strategy=strategy, redirect_uri=redirect_uri)


def psa(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            backend = request.matchdict.get("backend")
            if not backend:
                return HTTPNotFound("Missing backend")

            uri = redirect_uri
            if uri and not uri.startswith("/"):
                uri = request.route_url(uri, backend=backend)

            request.strategy = load_strategy(request)
            request.backend = load_backend(request.strategy, backend, uri)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        is_logged_in = module_member(  # fmt: skip
            request.backend.setting("LOGGEDIN_FUNCTION")
        )
        if not is_logged_in(request):
            raise HTTPForbidden("Not authorized user")
        return func(request, *args, **kwargs)

    return wrapper


def backends(request, user):
    """
    Load Social Auth current user data to context under the key 'backends'.
    Will return the output of social_core.backends.utils.user_backends_data.
    """
    storage = module_member(get_helper("STORAGE"))
    return {
        "backends": user_backends_data(
            user, get_helper("AUTHENTICATION_BACKENDS"), storage
        )
    }


def strategy(*args, **kwargs):
    warnings.warn("@strategy decorator is deprecated, use @psa instead")
    return psa(*args, **kwargs)
