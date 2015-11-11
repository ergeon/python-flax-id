
FORWARD_TEMPLATE = '''
CREATE EXTENSION IF NOT EXISTS plv8;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE OR REPLACE FUNCTION gen_flax_id()
RETURNS text AS $$
    var TOTAL_BITS = 96;
    var EPOCH_START = Date.UTC(2015, 0, 1, 0, 0, 0);
    var TIMESTAMP_BITS = 40;
    var RANDOM_BITS = TOTAL_BITS - TIMESTAMP_BITS;
    var BASE64_ALPHABET = '-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz';

    var ms = (Date.now() - EPOCH_START).toString(2);
    ms = ms.toString(2);
    var random_bits = parseInt(plv8.execute("select encode(gen_random_bytes(7), 'hex')")[0].encode, 16);
    random_bits = random_bits.toString(2);
    while (random_bits.length < RANDOM_BITS) {{random_bits = '0' + random_bits}};
    var bnum = ms + random_bits;

    while (bnum.length < TOTAL_BITS) {{bnum = '0' + bnum}};
    var s = ''
    var i = 0;
    while (i<TOTAL_BITS) {{
        s += BASE64_ALPHABET[parseInt(bnum.slice(i, i+6), 2)];
        i += 6;
    }}
    return s;
$$ LANGUAGE plv8 VOLATILE STRICT;


CREATE OR REPLACE function set_flax_id_before_insert() returns TRIGGER LANGUAGE plpgsql as $$
begin
    new.{field_name} = gen_flax_id();
    return new;
end $$;


CREATE TRIGGER flax_id_on_insert BEFORE INSERT ON {model_name} FOR EACH ROW EXECUTE PROCEDURE set_flax_id_before_insert();
'''

REVERSE_TEMPLATE = '''
DROP TRIGGER flax_id_on_insert ON {model_name};
DROP function set_flax_id_before_insert();
DROP function gen_flax_id();
'''


def generate_migrations(model_name, field_name):
    return (
        FORWARD_TEMPLATE.format(model_name=model_name, field_name=field_name),
        REVERSE_TEMPLATE.format(model_name=model_name, field_name=field_name)
    )

