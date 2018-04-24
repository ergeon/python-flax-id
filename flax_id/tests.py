import time
import unittest

from datetime import datetime

from six.moves import range

from .flax_id import get_flax_id


class TestFlaxId(unittest.TestCase):

    def test_all_unique(self):
        # Not a rigorous test, just a sanity check
        ids = [get_flax_id() for _ in range(1000)]
        self.assertEqual(len(ids), len(set(ids)))

    def test_lexical_ordering(self):
        ids = []
        for year in range(datetime.today().year, 2030):
            for month in range(1, 12):
                for second in range(0, 60):
                    timestamp = time.mktime(
                        datetime(year, month, 1, 0, 0, second).timetuple()
                    )
                    ids.append(get_flax_id(timestamp))
        self.assertEqual(ids, sorted(ids))
