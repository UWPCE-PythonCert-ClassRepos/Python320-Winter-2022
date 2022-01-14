
import unittest


class TestListSorting(unittest.TestCase):

    sorted_list = [1, 3, 5, 6]
    #sample_list = [5, 1, 6, 3]

    def setUp(self):
        self.sample_list = [5, 1, 6, 3]

    # def tearDown(self):
    #     pass

    def test_sort(self):
        self.assertNotEqual(self.sample_list, self.sorted_list)
        self.assertNotEqual(self.sample_list, self.sorted_list[::-1])
        self.sample_list.sort()
        self.assertEqual(self.sample_list, self.sorted_list)

    def test_reverse_sort(self):

        self.sample_list.sort(reverse=True)
        self.assertEqual(self.sample_list, self.sorted_list[::-1])


if __name__ == '__main__':
    unittest.main()


