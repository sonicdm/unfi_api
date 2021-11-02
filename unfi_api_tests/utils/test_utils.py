from unittest import TestCase
from unfi_api.utils import index_header, round_retails



class TestIndexHeader(TestCase):

    def test_index_header_even_values(self):
        header = [["col1.1", "col1.2"], ["col2.1", "col2.2"]]
        expected = {
            0: "col1.1 col2.1",
            1: "col1.2 col2.2"
        }
        self.assertEqual(index_header(header), expected)

    def test_index_header_mismatched(self):
        header = [
            ["col1.1", "col1.2", "col1.3"], ["col2.1", "col2.2"]]
        expected = {
            0: "col1.1 col2.1",
            1: "col1.2 col2.2",
            2: "col1.3"
        }
        self.assertEqual(index_header(header), expected)
    
    def test_index_header_empty_first_row(self):
        header = [
            [], ["col2.1", "col2.2"]]
        expected = {
            0: "col2.1",
            1: "col2.2"
        }
        self.assertEqual(index_header(header), expected)

    def test_index_header_empty_last_row(self):
        header = [
            ["col1.1", "col1.2"], []]
        expected = {
            0: "col1.1",
            1: "col1.2"
        }
        self.assertEqual(index_header(header), expected)
    
    def test_index_header_three_rows(self):
        header = [
            ["col1.1", "col1.2"], ["col2.1", "col2.2"], ["col3.1", "col3.2"]]
        expected = {
            0: "col1.1 col2.1 col3.1",
            1: "col1.2 col2.2 col3.2"
        }
        self.assertEqual(index_header(header), expected)

    def test_index_header_three_rows_mismatched(self):
        header = [
            ["col1.1", "col1.2", "col1.3"], ["col2.1", "col2.2"], ["col3.1", "col3.2"]]
        expected = {
            0: "col1.1 col2.1 col3.1",
            1: "col1.2 col2.2 col3.2",
            2: "col1.3"
        }

    def test_index_header_with_first_row_first_col_empty(self):
        header = [
            ["","col1.2"], ["col2.1", "col2.2"]]
        expected = {
            0: "col2.1",
            1: "col1.2 col2.2"
        }
        self.assertEqual(index_header(header), expected)


class TestRoundRetails(TestCase):

    def test_round_retail_whole_number_ends_in_09(self):
        retail = "123.09"
        expected = 123.15
        self.assertEqual(round_retails(retail), expected)
    
    def test_round_retail_float_ends_in_05(self):
        retail = 123.05
        expected = 122.99
        self.assertEqual(round_retails(retail), expected)

    def test_round_retail_whole_number_string_ends_in_99(self):
        retail = 123.99
        expected = 123.99
        self.assertEqual(round_retails(retail), expected)
    
    def test_round_retail_1_cent_no_symbol(self):
        retail = ".01"
        expected = .05
        self.assertEqual(round_retails(retail), expected)
    
    def test_round_retail_1_cent_with_symbol(self):
        retail = "1¢"
        expected = .05
        self.assertEqual(round_retails(retail), expected)

    def test_round_retail_1_cent_float(self):
        retail = .01
        expected = .05
        self.assertEqual(round_retails(retail), expected)
    
    def test_round_retail_with_cent_symbol(self):
        retail = "34¢"
        expected = 0.35
        rounded = round_retails(retail)
        self.assertEqual(rounded, expected)

    def test_10_plus_cents(self):
        retail = .11
        expected = .15
        self.assertEqual(round_retails(retail), expected)

    def test_08_to_15(self):
        retail = 1.08
        expected = 1.15
        self.assertEqual(round_retails(retail), expected)
    
    def test_1_98_to_1_99(self):
        retail = 1.98
        expected = 1.99
        self.assertEqual(round_retails(retail), expected)

    def test_round_retail(self):
        retails_to_round = [
            123.09,
            123.05,
            123.99,
            ".01",
            "1¢",
            .01,
            .11,
            "34¢",
            1.03,
            1.08,
            1.98,
            1.33,
            1.22
        ]

        expected = [
            123.15,
            122.99,
            123.99,
            .05,
            .05,
            .05,
            .15,
            0.35,
            0.99,
            1.15,
            1.99,
            1.29,
            1.19
        ]
        
        for idx,retail in enumerate(retails_to_round):
            self.assertEqual(round_retails(retail), expected[idx])
