from unittest import TestCase

from stdnum import ean
from unfi_api.utils.upc import (
    stripcheckdigit,
)


class TestEAN13(TestCase):
    def setUp(self) -> None:
        self.example_ean_string_list = [
            "9421904-03404",
            "9421904-03403",
            "9421904-03401",
            "9421904-03400",
            "9353323-00092",
            "9353323-00089",
            "9353323-00079",
            "9353323-00076",
            "9327693-01025",
            "9327693-01024",
            "9327693-01023",
            "9327693-00952",
            "9327693-00951",
            "9327693-00904",
        ]

        self.example_ean_int_list = [
            int(x.replace("-", "")) for x in self.example_ean_string_list
        ]



class TestStripCheckDigit(TestCase):
    def setUp(self) -> None:
        self.upcs = [
            "027917-02352",
            "027917-02179",
            "027917-02168",
            "027917-02152",
            "027917-02058",
            "027917-01933",
            "027917-01694",
            "027917-01461",
            "027917-00885",
            "027917-00357",
            "027917-00139",
            "027917-00113",
            "027917-00112",
            "027917-00106",
            "027917-00000",
        ]

        self.int_upcs = [int(x.replace("-", "")) for x in self.upcs]
        self.no_check_upcs = [int(str(x)[:1]) for x in self.upcs]

    def test_stripcheckdigit(self):
        for idx,upc in enumerate(self.upcs):
            self.assertEqual(int(stripcheckdigit(upc)), self.int_upcs[idx])