import gzip
import xml.etree.ElementTree as ET


def parse_type(tag):
    return tag.split('}', maxsplit=1)[1]


def parse_vec(value):
    x, y, z = value.split()
    return {
        'x': float(x),
        'y': float(y),
        'z': float(z),
    }


def parse_rotation(value):
    x, y, z, w = value.split()
    return {
        'x': float(x),
        'y': float(y),
        'z': float(z),
        'w': float(w),
    }


def parse_boolean(value):
    if value == 'true':
        return {'true': True}
    if value == 'false':
        return {'true': False}
    raise ValueError(f'Cannot parse boolean value: "{value}"')


value_parsers = {
    'sfstring': lambda value: {'string': value},
    'boolean': parse_boolean,
    'sffloat': lambda value: {'value': float(value)},
    'sfint32': lambda value: {'value': int(value)},
    'sfvec3f': parse_vec,
    'sfrotation': parse_rotation,
}


def parse_element(element):
    attributes = element.attrib
    type_ = parse_type(element.tag)
    if 'value' in attributes:
        value = attributes.pop('value')
        attributes.update(value_parsers[type_](value))
    if 'timestamp' in attributes:
        attributes['timestamp'] = int(attributes['timestamp'])
    attributes['type'] = type_
    return attributes


def parse(filename):
    with gzip.open(filename) as f:
        for (_, element) in ET.iterparse(f):
            yield parse_element(element)
            element.clear()  # https://bugs.python.org/issue14762
