"""Linter rules checking entry field completeness."""
import itertools

from bibla.config import get_config
from bibla.rule import register_entry_rule


@register_entry_rule('M00', 'No authors or editors found')
def authors_present(key, entry, database):
    """Raise a linter warning when an entry has no authors or editors.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if author or editor fields are defined in the current
    entry, False otherwise
    """
    return bool(list(itertools.chain(*entry.persons.values())))


def register_variant_rule(entry_type, field, variant):
    rule_id = 'E10{}{}'.format(entry_type.capitalize(), field.capitalize())
    message = "Use `{}` instead of `{}`!".format(variant, field)

    @register_entry_rule(rule_id, message)
    def check_variant_field(key, entry, database, entry_type=entry_type, field=field, variant=variant):
        """Raise a linter warning when a specific field is used instead of its variant.

        This function checks if the variant field is required and if the specific field is present.
        If these conditions are met, it suggests to use the variant field instead of the specific field.

        :param key: The key of the current bibliography entry
        :param entry: The current bibliography entry
        :param database: All bibliography entries
        :param entry_type: Anchor variable to pass the local variable `entry_type` from outer scope
        :param field: The field that is being checked
        :param variant: The field that should be used instead
        :return: False if the specific field is used instead of its variant, True otherwise
        """
        if entry.type == entry_type and field in entry.fields:
            return False
        else:
            return True


for entry_type, spec in get_config()['type_spec'].items():
    for req_field in spec['required']:
        rule_id = 'M01{}{}'.format(entry_type.capitalize(), req_field.capitalize())
        message = 'Missing required field `{}` for entry type `{}`'.format(req_field, entry_type)

        @register_entry_rule(rule_id, message)
        def check_required_field_present(key, entry, database, entry_type=entry_type, req_field=req_field):
            """Raise a linter warning when not all required fields are present.

            Required fields for an entry type are defined in the configuration
            with the `required` list of field types for a specific entry
            type  in the `type_spec` dictionary.

            :param key: The key of the current bibliography entry
            :param entry: The current bibliography entry
            :param database: All bibliography entries
            :param entry_type: Anchor variable to pass the local variable `entry_type` from outer scope
            :param req_field: Anchor variable to pass the local variable `req_field` from outer scope
            :return: True if the current entry contains all required fields, False otherwise
            """
            if entry.type == entry_type:
                return req_field in entry.fields
            else:
                return True

        alternate_fields = get_config()['alternate_fields']
        if req_field in alternate_fields:
            for alt_field in alternate_fields[req_field]:
                register_variant_rule(entry_type, alt_field, req_field)

    for opt_field in spec['optional']:
        rule_id = 'M02{}{}'.format(entry_type.capitalize(), opt_field.capitalize())
        message = 'Missing optional field `{}` for entry type `{}`'.format(opt_field, entry_type)

        @register_entry_rule(rule_id, message)
        def check_optional_field_present(key, entry, database, entry_type=entry_type, opt_field=opt_field):
            """Raise a linter warning when not all optional fields are present.

            Optional fields for an entry type are defined in the configuration
            with the `optional` list of field types for a specific entry
            type  in the `type_spec` dictionary.

            :param key: The key of the current bibliography entry
            :param entry: The current bibliography entry
            :param database: All bibliography entries
            :param entry_type: Anchor variable to pass the local variable `entry_type` from outer scope
            :param opt_field: Anchor variable to pass the local variable `opt_field` from outer scope
            :return: True if the current entry contains all optional fields, False otherwise
            """
            if entry.type == entry_type:
                return opt_field in entry.fields
            else:
                return True


@register_entry_rule('M03', 'Special characters should be replaced by the command to generate them: %, &, $, #, _, \\, ~, ^, |')
def check_special_characters(key, entry, database):
    """Raise a linter warning when a field contains special characters that should be replaced.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if no field contains special characters, False otherwise.
    """
    special_chars = ['%', '&', '$', '#', '_', '\\', '~', '^', '|']
    fields_to_ignore = ['url', 'doi', 'file', 'eprint', 'issn', 'isbn', 'note', 'abstract', 'keywords']

    for field_name, field_value in entry.fields.items():
        if field_name in fields_to_ignore: 
            return True
        if any(char in field_value for char in special_chars):
            for char in special_chars:
                if char in field_value and field_value[field_value.index(char) - 1] != '\\':
                    return False
    return True
