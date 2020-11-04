from bibl.config import get_config
from bibl.rule import register_entry_rule


@register_entry_rule('U00', 'Unrecognized entry type')
def entry_type(key, entry, database):
    return entry.type in get_config()['type_spec'].keys()


for entry_type, spec in get_config()['type_spec'].items():
    id = 'U01{}'.format(entry_type.capitalize())

    @register_entry_rule(id, 'Unrecognized field type for entry type `{}`'.format(entry_type))
    def field_type(key, entry, database, entry_type=entry_type):
        if entry.type == entry_type and entry.type in get_config()['type_spec'].keys():
            optional_fields = get_config()['type_spec'][entry.type]['optional']
            required_fields = get_config()['type_spec'][entry.type]['required']
            for field_type in entry.fields.keys():
                if not field_type in optional_fields and not field_type in required_fields:
                    return False
        return True
