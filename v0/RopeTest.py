import unittest
from v0.Rope import Rope


class TestRopeMethods(unittest.TestCase):

    def test_collectleaves(self):
        rope_data = "Je suis"
        rope = Rope(rope_data)
        result = rope.collectleaves()
        self.assertEqual(result, rope_data, "Collecting leaves did not return the expected result.")

    def test_insert(self):
        rope_data = "Je suis"
        rope = Rope(rope_data)
        rope.insert(3, " content")
        result = rope.collectleaves()
        expected_result = "Je content suis"
        self.assertEqual(result, expected_result, "Insertion did not produce the expected result.")

    def test_delete(self):
        rope_data = "Je suis content"
        rope = Rope(rope_data)
        rope.delete(3, 7)
        result = rope.collectleaves()
        expected_result = "Je content"
        self.assertEqual(result, expected_result, "Deletion did not produce the expected result.")

    def test_index(self):
        rope_data = "Je suis"
        rope = Rope(rope_data)
        result = rope.index(3)
        expected_result = "s"
        self.assertEqual(result, expected_result, "Indexing did not produce the expected result.")

    def test_concatRope(self):
        rope_data1 = "Je "
        rope_data2 = "suis"
        rope1 = Rope(rope_data1)
        rope2 = Rope(rope_data2)
        rope1.concatRope(rope2)
        result = rope1.collectleaves()
        expected_result = "Je suis"
        self.assertEqual(result, expected_result, "Concatenation did not produce the expected result.")

    # Add more test methods for other functions as needed...

if __name__ == '__main__':
    unittest.main()
