# -*- coding: utf-8 -*-

from app import create_app
import unittest
import json


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

    def test_hello_version(self):
        limit = 5
        timeout = 120
        resp = self.app.test_client().get(
            "/ok/friends?id=550419762162&limit="
            + str(limit)
            + "&timeout="
            + str(timeout)
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, "application/json")
        self.assertIn("name", str(resp.data))
        self.assertIn(bytes("Недомеркова", "utf-8"), resp.data)
        resp_dict = json.loads(resp.data)
        self.assertEqual(len(resp_dict["result"]), limit)


if __name__ == "__main__":
    unittest.main(warnings="ignore")
