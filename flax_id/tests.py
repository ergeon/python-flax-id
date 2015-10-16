import unittest
from datetime import datetime
import time

from flax_id import get_flax_id


class FlaxIdTest(unittest.TestCase):

    def test_all_unique(self):
        # Not a rigorous test, just a sanity check
        ids = [get_flax_id() for _ in xrange(1000)]
        self.assertEquals(len(ids), len(set(ids)))

    def test_lexical_ordering(self):
        ids = []
        for year in range(2015, 2030):
            for month in range(1, 12):
                for second in range(0, 60):
                    timestamp = time.mktime(datetime(year, month, 1, 0, 0, second).timetuple())
                    ids.append(get_flax_id(timestamp))
        self.assertEquals(ids, sorted(ids))


if __name__ == '__main__':
    unittest.main()
