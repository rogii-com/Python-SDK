import os
import re

THEME_SCRIPT = re.compile(
    r'<script>\s*document\.body\.dataset\.theme\s*=\s*localStorage\.getItem\("theme"\)\s*\|\|\s*"auto";\s*</script>',
    re.DOTALL,
)


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


def skip_inline_theme_script(app, exception):
    if exception or app.builder.name != 'html':
        return

    outdir = app.builder.outdir

    for root, _, files in os.walk(outdir):
        for fname in files:
            if not fname.endswith('.html'):
                continue

            path = os.path.join(root, fname)

            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()

            new_text = THEME_SCRIPT.sub('', text)

            if text != new_text:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_text)
