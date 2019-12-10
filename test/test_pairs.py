import unittest
from sbmtools import PairsList, AbstractAtomPair


class TestPairs(unittest.TestCase):

    def test_init(self):
        # Initiate with a list of iterables.
        p1 = PairsList([[1, 2], [1, 3], [2, 3]])

        # Initiate with a list of AbstractAtomPair objects.
        ap1 = AbstractAtomPair(1, 2)
        ap2 = AbstractAtomPair(1, 3)
        ap3 = AbstractAtomPair(2, 3)

        p1 = PairsList([ap1, ap2, ap3])

    def test_add(self):
        ap1 = AbstractAtomPair(1, 2)
        ap2 = AbstractAtomPair(2, 2)
        ap3 = AbstractAtomPair(3, 2)
        ap4 = AbstractAtomPair(4, 2)
        ap5 = AbstractAtomPair(5, 2)

        p1 = PairsList([ap1, ap2, ap3, ap4])
        p2 = PairsList([ap1, ap2, ap5])

        p3 = p1 + p2
        self.assertEqual(p3, PairsList([ap1, ap2, ap3, ap4, ap1, ap2, ap5]))

        p3 = p1.add(p2)
        self.assertEqual(p3, PairsList([ap1, ap2, ap3, ap4, ap1, ap2, ap5]))

    def test_remove(self):
        ap1 = AbstractAtomPair(1, 2)
        ap2 = AbstractAtomPair(2, 2)
        ap3 = AbstractAtomPair(3, 2)
        ap4 = AbstractAtomPair(4, 2)
        ap5 = AbstractAtomPair(5, 2)

        p1 = PairsList([ap1, ap2, ap3, ap4])
        p2 = PairsList([ap1, ap2, ap5])

        p3 = p1 - p2
        self.assertEqual(p3, PairsList([ap3, ap4]))

        p3 = p1.remove(p2)
        self.assertEqual(p3, PairsList([ap3, ap4]))

    def test_union(self):
        ap1 = AbstractAtomPair(1, 2)
        ap2 = AbstractAtomPair(2, 2)
        ap3 = AbstractAtomPair(3, 2)
        ap4 = AbstractAtomPair(4, 2)
        ap5 = AbstractAtomPair(5, 2)

        p1 = PairsList([ap1, ap2, ap3, ap4])
        p2 = PairsList([ap1, ap2, ap5])

        p3 = p1.union(p2)
        self.assertEqual(p3, PairsList([ap1, ap2, ap3, ap4, ap5]))

    def test_intersection(self):
        ap1 = AbstractAtomPair(1, 2)
        ap2 = AbstractAtomPair(2, 2)
        ap3 = AbstractAtomPair(3, 2)
        ap4 = AbstractAtomPair(4, 2)
        ap5 = AbstractAtomPair(5, 2)

        p1 = PairsList([ap1, ap2, ap3, ap4])
        p2 = PairsList([ap1, ap2, ap5])

        p3 = p1.intersection(p2)
        self.assertEqual(p3, PairsList([ap1, ap2]))

    def test_symmetric_difference(self):
        ap1 = AbstractAtomPair(1, 2)
        ap2 = AbstractAtomPair(2, 2)
        ap3 = AbstractAtomPair(3, 2)
        ap4 = AbstractAtomPair(4, 2)
        ap5 = AbstractAtomPair(5, 2)

        p1 = PairsList([ap1, ap2, ap3, ap4])
        p2 = PairsList([ap1, ap2, ap5])

        p3 = p1.symmetric_difference(p2)
        self.assertEqual(p3, PairsList([ap3, ap4, ap5]))


if __name__ == '__main__':
    unittest.main()
