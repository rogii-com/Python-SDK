from sphinx.util.osutil import relative_uri

from .python_doc_names import section_titles

main_classes = [
    'Base',
    'Client',
    'Comment',
    'Earth model',
    'Horizon',
    'Interpretation',
    'Log',
    'Mudlog',
    'Project',
    'Target line',
    'Topset',
    'Trajectory',
    'Types',
    'Well',
]


def capitalize_after_space(s: str) -> str:
    return ' '.join(word.capitalize() for word in s.split(' '))


def sidebar_settings(app, pagename, templatename, context, doctree):
    main_section_titles_and_links = []
    wells_section_titles_and_links = []

    if not main_section_titles_and_links:
        for file_name in section_titles:
            target_path = f'autoapi/rogii_solo/{file_name}/index.html'
            link = relative_uri(pagename, target_path)
            title = capitalize_after_space(file_name.replace('_', ' '))

            if title in main_classes:
                main_section_titles_and_links.append({'title': title, 'link': link})
            else:
                wells_section_titles_and_links.append({'title': title, 'link': link})

    context['main_section_titles_and_links'] = main_section_titles_and_links
    context['wells_section_titles_and_links'] = wells_section_titles_and_links
