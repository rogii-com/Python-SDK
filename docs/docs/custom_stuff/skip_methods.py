def skip_methods(app, what, name, obj, skip, options):
    """
    Skip all dunder methods from the documentation.
    """
    if what in ('method', 'attribute'):
        method_name = name.rsplit('.', 1)[-1]

        if method_name.startswith('__') or method_name.startswith('_'):
            return True

    return None
