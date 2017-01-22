__version__ = '1.0.0'

def includeme(config):
    from social_core.utils import setting_name

    if config.registry.settings.get(setting_name('TRAILING_SLASH')):
        extra = '/'
    else:
        extra = ''

    config.add_route('social.auth', '/login/{backend}' + extra)
    config.add_route('social.complete', '/complete/{backend}' + extra)
    config.add_route('social.disconnect', '/disconnect/{backend}' + extra)
    config.add_route('social.disconnect_association',
                     '/disconnect/{backend}/{association_id}' + extra)
