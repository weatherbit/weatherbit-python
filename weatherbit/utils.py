import sys
import re


class UnicodeMixin(object):

    """Mixin class to handle defining the proper __str__/__unicode__
    methods in Python 2 or 3."""

    if sys.version_info[0] >= 3:  # Python 3
        def __str__(self):
            return super().__str__()
    else:  # Python 2
        def __str__(self):
            return super().__str__().encode('utf8')

class PropertyUnavailable(AttributeError):
	pass

def is_valid_day_format(input_string):
    pattern = re.compile(r'^\d{2}-\d{2}$')
    return bool(pattern.match(input_string))
