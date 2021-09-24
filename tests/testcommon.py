# -*- coding: utf-8 -*-
import unittest
import os
import time
from common import get_proxy, parse_html, get_html


class TestPrepairProxy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        args = {}
        args["id"] = 550419762162
        args["timeout"] = 120
        args["limit"] = 5
        args["start_time"] = time.time()
        args["login"] = "79112587299"
        args["password"] = "19734682"
        args["proxy_str"] = get_proxy.get_free_proxy(args)
        cls.element_html = get_html.get_ok_friends_html(args).decode("utf-8")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_html_from_web(self):
        arr = parse_html.parse_friends_html(self.element_html, 3)
        self.assertEqual(len(arr), 3)
        self.assertIsInstance(arr[0]["id"], str)
        self.assertIsInstance(arr[0]["name"], str)

    def test_parse_html_from_file(self):
        html_file_str = "tests/raw.html"
        if os.path.exists(html_file_str):
            with open(html_file_str, "r") as file_obj:
                html = file_obj.read()
            arr = parse_html.parse_friends_html(html, 3)
            self.assertEqual(len(arr), 3)
            self.assertEqual(arr[0]["id"], "539888393882")
            self.assertEqual(arr[0]["name"], "Татьяна Недомеркова")
            self.assertEqual(
                arr[0]["image"],
                "http://i.mycdn.me/i?r=AzExTCcIQuhnRIX9gBwt8KAMPvnrd56mpxGD0HfjL3wk_ejO_o5Z4HGYrK16ZgQJHhI&fn=sqr_128",
            )
        else:
            raise AssertionError("File does not exist: %s" % str(html_file_str))


if __name__ == "__main__":
    unittest.main()
