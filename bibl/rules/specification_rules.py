from bibl.config import get_config
from bibl.rule import register_entry_rule


@register_entry_rule('S00', 'Unrecognized entry type')
def entry_type(key, entry, database):
    return entry.entry_type in get_config()['type_spec'].keys()


for entry_type, spec in get_config()['type_spec'].items():
    for req_field in spec['required']:
        id = 'S01{}'.format(entry_type.capitalize())


        @register_entry_rule(id, 'Unrecognized field type for entry type `{}`'.format(entry_type))
        def field_type(key, entry, database, type=entry_type, ):
            if entry.entry_type == entry_type and entry.entry_type in get_config()['type_spec'].keys():
                optional_fields = get_config()['type_spec'][entry.entry_type]['optional'].keys()
                required = get_config()['type_spec'][entry.entry_type]['required'].keys()
                for field_type in entry.fields.keys():
                    if not field_type in optional_fields and not field_type in required:
                        return False
            return True
