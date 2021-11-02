from unittest import TestCase
from unfi_api.utils.string import clean_size_field



class TestUtils(TestCase):

    def test_clean_size_field(self):
        size_with_three_slashes = "12/6/12 oz"
        size_with_two_slashes = "12/12 oz"
        size_with_no_slashes = "12 oz"

        self.assertEqual(clean_size_field(None), None)