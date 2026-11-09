import unittest
from datetime import date, timedelta

from medit.schedule import order_for_cycle, passage_id_for

IDS = [f"p{i}" for i in range(480)]
SMALL = ["a", "b", "c"]
START = date(2026, 11, 10)


class ScheduleTest(unittest.TestCase):
    def test_cycle_is_permutation(self):
        for c in range(6):
            self.assertEqual(sorted(order_for_cycle(IDS, c)), sorted(IDS))

    def test_cycles_differ(self):
        orders = [tuple(order_for_cycle(IDS, c)) for c in range(6)]
        self.assertEqual(len(set(orders)), 6)

    def test_deterministic(self):
        self.assertEqual(order_for_cycle(IDS, 3), order_for_cycle(list(IDS), 3))

    def test_does_not_mutate_input(self):
        ids = list(IDS)
        order_for_cycle(ids, 2)
        self.assertEqual(ids, IDS)

    def test_no_back_to_back_across_boundary(self):
        for ids in (IDS, SMALL):
            for c in range(51):
                self.assertNotEqual(order_for_cycle(ids, c)[-1], order_for_cycle(ids, c + 1)[0], (len(ids), c))

    def test_day_mapping(self):
        for k in (0, 1, 479, 480, 961):
            self.assertEqual(passage_id_for(START + timedelta(days=k), START, IDS),
                             order_for_cycle(IDS, k // 480)[k % 480])

    def test_before_start_raises(self):
        with self.assertRaises(ValueError):
            passage_id_for(START - timedelta(days=1), START, IDS)


if __name__ == "__main__":
    unittest.main()
