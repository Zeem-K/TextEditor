import pytest
from Rope import Rope  # Adjust the import based on your Rope class location

# Test the creation of a Rope and basic reporting
def test_rope_creation_and_basic_reporting():
    rope = Rope("Hello World")
    assert rope.report(0, 11) == "Hello World", "Initial string should be 'Hello World'"

# Test inserting text into the Rope
@pytest.mark.parametrize("original, insert_text, index, expected", [
    ("Hello World", " Beautiful", 5, "Hello Beautiful World"),
    ("", "Hello World", 0, "Hello World"),  # Insert into empty
    ("World", "Hello ", 0, "Hello World"),  # Insert at start
    ("Hello", " World!", 5, "Hello World!")  # Insert at end
])
def test_insert(original, insert_text, index, expected):
    rope = Rope(original)
    rope.insert(index, insert_text)
    assert rope.report(0, len(expected)) == expected

# Test deleting text from the Rope
@pytest.mark.parametrize("original, start_index, length, expected", [
    ("Hello Beautiful World", 5, 10, "Hello World"),
    ("Hello World!", 0, 6, "World!"),  # Delete at start
    ("Hello World!", 6, 6, "Hello "),  # Delete at end
    ("", 0, 10, ""),  # Delete from empty
])
def test_delete(original, start_index, length, expected):
    rope = Rope(original)
    rope.delete(start_index, length)
    assert rope.report(0, len(expected)) == expected

# Test reporting a substring from the Rope
@pytest.mark.parametrize("original, start_index, end_index, expected", [
    ("Hello Beautiful World", 6, 15, "Beautiful"),
    ("", 0, 0, ""),  # Report from empty
    ("Hello World", 0, 5, "Hello")  # Report at start
])
def test_report_substring(original, start_index, end_index, expected):
    rope = Rope(original)
    substring = rope.report(start_index, end_index)
    assert substring == expected

# Test concatenating two Ropes
def test_concatenate():
    rope1 = Rope("Hello")
    rope2 = Rope(" World")
    rope1.concatenate(rope1, rope2)
    assert rope1.report(0, 11) == "Hello World", "Concatenated string should be 'Hello World'"

# Test handling of large input
def test_large_input():
    large_string = "a" * 10000  # A string of 10,000 'a's
    rope = Rope(large_string)
    rope.insert(5000, "b" * 1000)  # Insert 1,000 'b's at the middle
    assert rope.report(4999, 5002) == "abb", "Large input handling should work correctly"

# Optional: Test for out-of-bounds insert/delete
# These tests are expected to raise exceptions, demonstrating how to test error conditions
def test_insert_out_of_bounds():
    rope = Rope("Hello")
    with pytest.raises(IndexError):
        rope.insert(100, "World")

def test_delete_out_of_bounds():
    rope = Rope("Hello")
    with pytest.raises(IndexError):
        rope.delete(100, 10)
