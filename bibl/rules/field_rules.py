import itertools

from bibl.config import get_config
from bibl.rule import register_entry_rule


@register_entry_rule('M00', 'No authors or editors found')
def authors(key, entry, database):
    return bool(list(itertools.chain(*entry.persons.values())))


for entry_type, spec in get_config()['type_spec'].items():
    for req_field in spec['required']:
        rule_id = 'M01{}{}'.format(entry_type.capitalize(),
                                   req_field.capitalize())
        message = 'Missing required field `{}` for entry type `{}`'
        message = message.format(req_field, entry_type)


        @register_entry_rule(rule_id, message)
        def check_required_field_present(
                key, entry, database,
                entry_type=entry_type,
                req_field=req_field):
            if entry.type == entry_type:
                return req_field in entry.fields
            else:
                return True

    for opt_field in spec['optional']:
        rule_id = 'M02{}{}'.format(entry_type.capitalize(),
                                   opt_field.capitalize())
        message = 'Missing optional field `{}` for entry type `{}`'
        message = message.format(opt_field, entry_type)


        @register_entry_rule(rule_id, message)
        def check_optional_field_present(
                key, entry, database,
                entry_type=entry_type,
                opt_field=opt_field):
            if entry.type == entry_type:
                return opt_field in entry.fields
            else:
                return True
