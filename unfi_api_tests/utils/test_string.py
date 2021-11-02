from typing import Type
from unittest import TestCase

from unfi_api.utils.string import (camel_to_snake_case, clean_size_field,
                                   convert_strings_to_number, is_hex,
                                   is_hexcolor, isnumber,
                                   pascal_case_to_snake_case,
                                   remove_escaped_characters, string_to_snake,
                                   strings_to_numbers)


class TestCleanSizeField(TestCase):

    def test_clean_size_field(self):
        size_with_three_slashes = "12/6/12 oz"
        size_with_two_slashes = "12/12 oz"
        size_with_no_slashes = "12 oz"
        non_string_input = 12

        self.assertEqual(clean_size_field(None), None)
        self.assertEqual(clean_size_field(size_with_three_slashes), "6/12 oz")
        self.assertEqual(clean_size_field(size_with_two_slashes), "12 oz")
        self.assertEqual(clean_size_field(size_with_no_slashes), "12 oz")
        self.assertEqual(clean_size_field(non_string_input), 12)

    def test_clean_size_field_with_invalid_input(self):
        invalid_input = lambda: print("y")
        self.assertEqual(clean_size_field(invalid_input), invalid_input)


class TestHex(TestCase):

    def test_is_hex_true(self):
        self.assertTrue(is_hex("#000000"))
    
    def test_is_hex_false(self):
        self.assertFalse(is_hex("NOT HEX AT ALL"))

    def test_is_hex_color_true(self):
        self.assertTrue(is_hexcolor("#000000"))
        self.assertTrue(is_hexcolor("#FFF"))
    
    def test_is_hex_color_false(self):
        self.assertFalse(is_hexcolor("NOT HEX AT ALL"))
        self.assertFalse(is_hexcolor("#FF000"))
        self.assertFalse(is_hexcolor("#FF"))

    def test_is_hex_non_string_input(self):
        self.assertFalse(is_hex(12345))

class TestStringsToNumbers(TestCase):

    def test_strings_to_numbers_only_numbers(self):
        self.assertEqual(strings_to_numbers(["1", "2", "3"]), [1, 2, 3])

    def test_strings_to_numbers_with_non_numbers(self):
        self.assertEqual(strings_to_numbers(["1", "2", "3", "a"]), [1, 2, 3, "a"])

    def test_strings_to_numbers_with_non_numbers_and_empty_strings(self):
        self.assertEqual(strings_to_numbers(["1", "2", "3", "", "a"]), [1, 2, 3, "", "a"])

    def test_strings_to_numbers_with_non_numbers_and_empty_strings_and_none(self):
        self.assertEqual(strings_to_numbers(["1", "2", "3", "", None, "a"]), [1, 2, 3, "", None, "a"])


class TestStringCasing(TestCase):

    def test_string_to_snake(self):
        self.assertEqual(string_to_snake("Test String"), "test_string")

    def test_string_to_snake_case_with_non_string_input(self):
        self.assertEqual(string_to_snake(12345), 12345)

    def test_camel_to_snake_case(self):
        self.assertEqual(camel_to_snake_case("TestString"), "test_string")
        self.assertEqual(camel_to_snake_case("test_string"), "test_string")
        self.assertEqual(camel_to_snake_case("testString"), "test_string")

class TestIsNumber(TestCase):

    def test_isnumber_true(self):
        self.assertTrue(isnumber(1))
        self.assertTrue(isnumber(1.2))
        self.assertTrue(isnumber(1.2e3))
        self.assertTrue(isnumber("1.2"))
        self.assertTrue(isnumber("1.2e3"))
        self.assertTrue(isnumber("69"))

    def test_isnumber_false(self):
        self.assertFalse(isnumber("a"))
        self.assertFalse(isnumber("1a"))
        self.assertFalse(isnumber("1.2.3"))
        self.assertFalse(isnumber(dict()))


class TestRemoveEscapedCharacters(TestCase):

    def test_remove_escaped_characters_new_line(self):
        self.assertEqual(remove_escaped_characters("\n"), "")

    def test_remove_escaped_characters_tab(self):
        self.assertEqual(remove_escaped_characters("\t"), "")

    def test_remove_escaped_characters_carriage_return(self):
        self.assertEqual(remove_escaped_characters("\r"), "")

    def test_remove_escaped_characters_mixed_string(self):
        self.assertEqual(remove_escaped_characters("\n\t\r"), "")

    def test_remove_escaped_characters_empty_string(self):
        self.assertEqual(remove_escaped_characters(""), "")

    def test_remove_escaped_characters_string_with_no_escaped_characters(self):
        self.assertEqual(remove_escaped_characters("This is a test"), "This is a test")

    def test_remove_escaped_characters_string_with_escaped_characters(self):
        self.assertEqual(remove_escaped_characters("This is a \n test"), "This is a  test")

    def test_remove_escaped_characters_string_with_double_escaped_characters(self):
        self.assertEqual(remove_escaped_characters("This is a \\n  \\t \\r test"), "This is a     test")       

    def test_remove_escaped_characters_non_string_input(self):
        with self.assertRaises(TypeError):
            remove_escaped_characters(12345)


