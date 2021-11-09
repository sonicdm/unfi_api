from unittest import TestCase
from unfi_api.utils import index_header, round_retails, yesno, explode_number


class TestIndexHeader(TestCase):
    def test_index_header_even_values(self):
        header = [["col1.1", "col1.2"], ["col2.1", "col2.2"]]
        expected = {0: "col1.1 col2.1", 1: "col1.2 col2.2"}
        self.assertEqual(index_header(header), expected)

    def test_index_header_mismatched(self):
        header = [["col1.1", "col1.2", "col1.3"], ["col2.1", "col2.2"]]
        expected = {0: "col1.1 col2.1", 1: "col1.2 col2.2", 2: "col1.3"}
        self.assertEqual(index_header(header), expected)

    def test_index_header_empty_first_row(self):
        header = [[], ["col2.1", "col2.2"]]
        expected = {0: "col2.1", 1: "col2.2"}
        self.assertEqual(index_header(header), expected)

    def test_index_header_empty_last_row(self):
        header = [["col1.1", "col1.2"], []]
        expected = {0: "col1.1", 1: "col1.2"}
        self.assertEqual(index_header(header), expected)

    def test_index_header_three_rows(self):
        header = [["col1.1", "col1.2"], ["col2.1", "col2.2"], ["col3.1", "col3.2"]]
        expected = {0: "col1.1 col2.1 col3.1", 1: "col1.2 col2.2 col3.2"}
        self.assertEqual(index_header(header), expected)

    def test_index_header_three_rows_mismatched(self):
        header = [
            ["col1.1", "col1.2", "col1.3"],
            ["col2.1", "col2.2"],
            ["col3.1", "col3.2"],
        ]
        expected = {0: "col1.1 col2.1 col3.1", 1: "col1.2 col2.2 col3.2", 2: "col1.3"}

    def test_index_header_with_first_row_first_col_empty(self):
        header = [["", "col1.2"], ["col2.1", "col2.2"]]
        expected = {0: "col2.1", 1: "col1.2 col2.2"}
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
        expected = 0.05
        self.assertEqual(round_retails(retail), expected)

    def test_round_retail_1_cent_with_symbol(self):
        retail = "1¢"
        expected = 0.05
        self.assertEqual(round_retails(retail), expected)

    def test_round_retail_1_cent_float(self):
        retail = 0.01
        expected = 0.05
        self.assertEqual(round_retails(retail), expected)

    def test_round_retail_with_cent_symbol(self):
        retail = "34¢"
        expected = 0.35
        rounded = round_retails(retail)
        self.assertEqual(rounded, expected)

    def test_10_plus_cents(self):
        retail = 0.11
        expected = 0.15
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
            0.01,
            0.11,
            "34¢",
            1.03,
            1.08,
            1.98,
            1.33,
            1.22,
            2.12,
        ]

        expected = [
            123.15,
            122.99,
            123.99,
            0.05,
            0.05,
            0.05,
            0.15,
            0.35,
            0.99,
            1.15,
            1.99,
            1.29,
            1.19,
            2.15,
        ]

        for idx, retail in enumerate(retails_to_round):
            self.assertEqual(round_retails(retail), expected[idx])

    def test_2_12_to_2_15(self):
        retail = 2.12
        expected = 2.15
        self.assertEqual(round_retails(retail), expected)


class TestYesNo(TestCase):
    def test_yes_no_yes_lowercase(self):
        self.assertEqual(yesno("yes"), True)

    def test_yes_no_no_lowercase(self):
        self.assertEqual(yesno("no"), False)

    def test_yes_no_default_false(self):
        self.assertEqual(yesno("", False), False)

    def test_yes_no_default_true(self):
        self.assertEqual(yesno("", True), True)

    def test_yes_no_yes_uppercase(self):
        self.assertEqual(yesno("YES"), True)

    def test_yes_no_no_uppercase(self):
        self.assertEqual(yesno("NO"), False)

    def test_yes_no_yes_mixed_case(self):
        self.assertEqual(yesno("YeS"), True)

    def test_yes_no_no_mixed_case(self):
        self.assertEqual(yesno("nO"), False)

    def test_yes_no_yes_with_spaces(self):
        self.assertEqual(yesno(" yes "), True)

    def test_yes_no_no_with_spaces(self):
        self.assertEqual(yesno(" no "), False)

    def test_yes_no_yes_with_spaces_uppercase(self):
        self.assertEqual(yesno(" YES "), True)

    def test_yes_no_no_with_spaces_uppercase(self):
        self.assertEqual(yesno(" NO "), False)

    def test_yes_no_yes_y(self):
        self.assertEqual(yesno("y"), True)

    def test_yes_no_no_n(self):
        self.assertEqual(yesno("n"), False)


class TestExplodeNumber(TestCase):
    def test_explode_number_zero(self):
        self.assertEqual(explode_number(0), (0, 0, 0))

    def test_explode_number_one(self):
        self.assertEqual(explode_number(1), (1, 0, 0))

    def test_explode_number_45_23(self):
        self.assertEqual(explode_number(45.23), (45, 2, 3))

    def test_explode_number_45_23231_with_decimal(self):
        self.assertEqual(explode_number(45.23231), (45, 2, 3))

    def test_explode_number_non_number_string(self):
        with self.assertRaises(TypeError):
            explode_number("abc")
