# Flax ID
# Reference Python implementation

# Clarity was chosen over the performance consideration,
# but it is fast enough to be used in most practical scenarios.

import calendar
import random
import time
from datetime import datetime

from six.moves import range

# The parameters below are really the part of the algorithm and are
# not expected to change

# Flax ID Regex
FLAX_ID_REGEX = '[-0-9A-Z_a-z]+'

# Total number of bits
TOTAL_BITS = 96
# We start from the year ezHome has started
EPOCH_START = datetime(2015, 1, 1)
# How many bits we reserve for the timestamp
TIMESTAMP_BITS = 40
# Remaining random bits
RANDOM_BITS = TOTAL_BITS - TIMESTAMP_BITS


# Modified Base 64 alphabet that preserves lexicographical ordering
BASE64_ALPHABET = (
    '-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '_abcdefghijklmnopqrstuvwxyz'
)


def get_flax_id_num(timestamp=None):
    """
    Generate a Flax ID number, using the provided timestamp
    or the current moment
    """
    # Get milliseconds fvalue for the epoch start
    epoch_ms = int(calendar.timegm(EPOCH_START.timetuple()) * 1000)
    # Get milliseconds from the start of the epoch
    ms = int((timestamp or time.time()) * 1000) - epoch_ms
    # Get random bits
    random_bits = random.getrandbits(RANDOM_BITS)
    # Combine random bits with the time bits
    id_num = (ms << RANDOM_BITS) + random_bits
    return id_num


def base64_lex_encode(num):
    """
    Take a number and encode it as a string using the custom Base64
    alphabet.
    """
    # Convert the number to binary and pad the zeroes
    bnum = format(num, 'b').zfill(TOTAL_BITS)
    s = ''
    for x in range(0, TOTAL_BITS, 6):
        s += BASE64_ALPHABET[int(bnum[x:x + 6], 2)]
    return s


def get_flax_id(timestamp=None):
    """
    Generate a string Flax ID, using the provided timestamp or the current
    moment.
    """
    return base64_lex_encode(get_flax_id_num(timestamp))


if __name__ == '__main__':
    import timeit
    print(
        timeit.timeit(
            'for x in range(1000): get_flax_id()',
            number=100,
            setup='from __main__ import get_flax_id'
        )
    )
