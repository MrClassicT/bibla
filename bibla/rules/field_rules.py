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


for entry_type, spec in get_config()['type_spec'].items():
    for req_field in spec['required']:
        rule_id = 'M01{}{}'.format(entry_type.capitalize(),
                                   req_field.capitalize())
        message = 'Missing required field `{}` for entry type `{}`'
        message = message.format(req_field, entry_type)

        @register_entry_rule(rule_id, message)
        def check_required_field_present(key, entry, database,
                                         entry_type=entry_type,
                                         req_field=req_field):
            """Raise a linter warning when not all required fields are present.

            Required fields for an entry type are defined in the configuration
            with the `required` list of field types for a specific entry
            type  in the `type_spec` dictionary.


            :param key: The key of the current bibliography entry
            :param entry: The current bibliography entry
            :param database: All bibliography entries
            :param entry_type: Anchor variable to pass the local
            variable `entry_type` from outer scope
            :param req_field: Anchor variable to pass the local variable
            `req_field`
            from outer scope
            :return: True if the current entry contains all required fields,
            False otherwise
            """
            if entry.type == entry_type:
                return req_field in entry.fields
            else:
                return True
