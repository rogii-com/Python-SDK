def skip_methods(app, what, name, obj, skip, options):
    """
    Delete the selected methods from the documentation.
    Delete type hints from method arguments.
    """
    exclusions = (
        '__iadd__',
        '__isub__',
    )

    exclude = False

    if '__init__' in name:
        return False

    if what == 'method':
        method_name = name.split('.')[2]
        exclude = method_name in exclusions
        obj.args = ', '.join([val[1] for val in obj.obj['args']])

    obj.skip = exclude

    return True if exclude else None
