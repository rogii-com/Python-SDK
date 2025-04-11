from docutils import nodes
from sphinx import addnodes
from sphinx.transforms import SphinxTransform

"""
Checks docstrings, and if it finds :displayname:
It replaces the function name in all locations in the generated documentation.
Used to replace the names of dunder methods with a more user-friendly syntax.
:displayname: in the docstring should be placed after the method description, separated by one blank line.

def __iter__(self):
    '''
    Iterate through grids.

    :displayname: for grid in Grids
    '''
"""


class ReplaceDescNameWithDisplayname(SphinxTransform):
    default_priority = 220
    debug = False

    def apply(self, **kwargs) -> None:
        if self.debug:
            # Saving a document to a file
            path = rf'_doc_debug/{self.document.children[0]["names"][0]}.xml'
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.document.pformat())

        # Initialization of a dictionary that you pass to a function
        self.ids_dict = {}
        self.process_all_desc_nodes(self.document)
        self.process_tables(self.document)

        if self.debug:

            # Saving a document to a file
            path = rf'_doc_debug/{self.document.children[0]["names"][0]}_result.xml'
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.document.pformat())

    def process_all_desc_nodes(self, node):
        for child in node.children:
            if isinstance(child, addnodes.desc):
                displayname = self.get_direct_displayname_from_desc(child)

                if displayname:
                    desc_name_node = self.get_desc_name_from_desc(child)
                    if desc_name_node:
                        original_name = desc_name_node.astext()
                        if self.debug:
                            print(f'Replacing desc_name "{original_name}" with "{displayname}"')
                        desc_name_node.clear()
                        desc_name_node += nodes.Text(displayname)

                        desc_signature = child.next_node(addnodes.desc_signature)
                        if desc_signature:
                            ids_dict = self.update_signature_attributes(desc_signature, original_name, displayname)

                            parameter_list_node = desc_signature.next_node(addnodes.desc_parameterlist)
                            if parameter_list_node:
                                desc_signature.remove(parameter_list_node)
                                if self.debug:
                                    print('Removed desc_parameterlist from desc_signature')

                    index_node = self.find_previous_index_node(child)
                    if index_node:
                        self.update_index_entries(index_node, original_name, displayname)

            self.process_all_desc_nodes(child)

    def process_tables(self, node):
        for table in node.traverse(nodes.table):
            if 'summarytable' in table.get('classes', []):
                self.process_table(table)

    def process_table(self, table_node):
        pass
        # Iterate over all nodes within the table
        for node in table_node.traverse():
            if isinstance(node, (nodes.reference, nodes.target)):
                original_refuri = node['refuri'].replace('#', '')
                if original_refuri in self.ids_dict:

                    # Replace attributes
                    new_refuri = '#' + self.ids_dict[original_refuri]
                    new_text = self.ids_dict[original_refuri].split('.')[-1]

                    node['refuri'] = new_refuri
                    if 'name' in node and node['name']:
                        node['name'] = new_refuri

                    if isinstance(node, nodes.reference):
                        node.clear()
                        node += nodes.Text(new_text)

                    elif isinstance(node, nodes.target):
                        node['ids'] = [new_text]
                        node['dupnames'] = [new_text]

                        # remove the function signature, including everything inside the parentheses and the parentheses themselves
                        for par_node in node.parent:
                            if isinstance(par_node, nodes.Text) and par_node.astext() != ' ':
                                par_node.parent.remove(par_node)

    def find_previous_index_node(self, desc_node):
        siblings = desc_node.parent.children
        desc_index = siblings.index(desc_node)

        for i in range(desc_index - 1, -1, -1):
            if isinstance(siblings[i], addnodes.index):
                return siblings[i]
        return None

    def get_direct_displayname_from_desc(self, desc_node):
        for content in desc_node.children:
            if isinstance(content, addnodes.desc_content):
                for field_list in content.children:
                    if isinstance(field_list, nodes.field_list):
                        for field in field_list.children:
                            field_name_node = field.next_node(nodes.field_name)
                            if field_name_node and field_name_node.astext().strip().lower() == 'displayname':
                                displayname = self.extract_displayname_from_field(field)
                                if field in field_list.children:
                                    field_list.remove(field)
                                    if self.debug:
                                        print('Removed field containing Displayname')
                                else:
                                    if self.debug:
                                        print('Field containing Displayname not found in field_list children.')
                                return displayname
        return None

    def get_desc_name_from_desc(self, desc_node):
        desc_signature = desc_node.next_node(addnodes.desc_signature)
        if desc_signature:
            return desc_signature.next_node(addnodes.desc_name)
        return None

    def extract_displayname_from_field(self, field_node: nodes.field) -> str:
        field_body = field_node.next_node(nodes.field_body)
        paragraph = field_body.next_node(nodes.paragraph)
        return paragraph.astext().strip()

    def update_signature_attributes(self, desc_signature, original_name, displayname):
        ids_dict = {}
        for attr_name, attr_value in desc_signature.attributes.items():
            if isinstance(attr_value, str) and original_name in attr_value:
                new_value = attr_value.replace(original_name, displayname)
                if attr_name == '_toc_name':
                    new_value = new_value.replace('()', '')

                if self.debug:
                    print(f'Updating attribute "{attr_name}": "{attr_value}" -> "{new_value}"')
                desc_signature[attr_name] = new_value
            elif isinstance(attr_value, list):
                new_value_list = [
                    item.replace(original_name, displayname).replace('()', '') if isinstance(item, str) and original_name in item else item
                    for item in attr_value
                ]
                if attr_name == 'ids':
                    ids_dict[attr_value[0]] = new_value_list[0]

                if new_value_list != attr_value and self.debug:
                    print(f'Updating attribute "{attr_name}": "{attr_value}" -> "{new_value_list}"')
                desc_signature[attr_name] = new_value_list

        if self.debug:
            print(f'Updating fullname: "{original_name}" -> "{displayname}"')
        desc_signature['fullname'] = displayname
        self.ids_dict.update(ids_dict)

    def update_index_entries(self, index_node, original_name, displayname):
        for i, entry in enumerate(index_node['entries']):
            updated_entry = tuple(
                item.replace(original_name, displayname).replace('()', '') if isinstance(item, str) and original_name in item else item
                for item in entry
            )
            if updated_entry != entry and self.debug:
                print(f'Updating index entry {i}: "{entry}" -> "{updated_entry}"')
            index_node['entries'][i] = updated_entry

def setup(app):
    app.add_transform(ReplaceDescNameWithDisplayname)
    app.add_config_value('debug', False, 'env')
