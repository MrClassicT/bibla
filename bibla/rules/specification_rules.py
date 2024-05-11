"""Linter rules checking consistency with entry and field type spec."""

from bibla.config import get_config
from bibla.rule import register_entry_rule


@register_entry_rule('U00', 'Unrecognized entry type')
def recognized_entry_type(key, entry, database):
    """Raise a linter warning when an entry type is not recognized.

    All recognized entry types are specified in the `type_spec` setting in the
    configuration.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if the type of the current bibliography entry is defined
    in the type specification
    """
    return entry.type in get_config()['type_spec'].keys()


for entry_type, spec in get_config()['type_spec'].items():
    rule_id = 'U01{}'.format(entry_type.capitalize())
    message = 'Unrecognized field type for entry type `{}`'.format(entry_type)

    @register_entry_rule(rule_id, message)
    def recognized_field_type(key, entry, database, entry_type=entry_type):
        """Raise a linter warning when field is not recognized for entry type.

        A rule of this type is generated for each entry type in the `type_spec`
        setting in the configuration.
        If a field type in a bibliography entry is not specified in the
        `required_fields` or `optional_fields` of the respective entry type,
        it is unrecognized and a warning wil be raised.

        :param key: The key of the current bibliography entry
        :param entry: The current bibliography entry
        :param database: All bibliography entries
        :param entry_type: Anchor variable to pass the local variable
        `entry_type` from outer scope
        :return: True if the types of all fields in the current bibliography
        entry are present in the required or optional fields of the
        specification of the type of that entry, False otherwise.
        """
        type_spec = get_config()['type_spec']
        available_types = type_spec.keys()
        if entry.type == entry_type and entry.type in available_types:
            optional_fields = type_spec[entry.type]['optional']
            required_fields = type_spec[entry.type]['required']
            for field_type in entry.fields.keys():
                if field_type not in optional_fields + required_fields:
                    return False
        return True
