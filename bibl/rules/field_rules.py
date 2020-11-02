import os
from bibl.rule import register_entry_rule
import yaml

with open(os.path.join(os.path.dirname(__file__), 'type_spec.yml')) as type_spec_file:
    TYPES = yaml.load(type_spec_file, Loader=yaml.FullLoader)

for type, spec in TYPES.items():
    for req_field in spec['required']:
        id = 'F01{}{}'.format(type.capitalize(), req_field.capitalize())


        @register_entry_rule(id, 'Missing required field {} for entry type {}'.format(req_field, type))
        def check_required_field_present(key, entry, database, type=type, req_field=req_field):
            if entry.type == type:
                return req_field in entry.fields
            else:
                return True
        
    for opt_field in spec['optional']:
        id = 'F02{}{}'.format(type.capitalize(), opt_field.capitalize())


        @register_entry_rule(id, 'Missing required field {} for entry type {}'.format(opt_field, type))
        def check_optional_field_present(key, entry, database, type=type, opt_field=opt_field):
            if entry.type == type:
                return opt_field in entry.fields
            else:
                return True
