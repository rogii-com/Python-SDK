def skip_methods(app, what, name, obj, skip, options):
    if what in ('method', 'attribute', 'data', 'attributes'):
        method_name = name.rsplit('.', 1)[-1]

        if method_name.startswith(('__', '_')):
            return True

        if what in ['data', 'attributes']:
            return True

    if what in ('abstract'):
        return True

    return None
