#!/usr/bin/env python3

import unittest
import os

import xadmin

sampledata = """
911       emergency    emergency@nowhere.com

22222222  peppes       pizza@peppes.com
1234      booty        bootycall@jalla.com
"""

tmpfile = "testdata.txt"

class TestXadmin(unittest.TestCase):

    def setUp(self):
        with open(tmpfile, 'w') as file:
            file.write(sampledata)
        xadmin.endpoints_file = tmpfile
        
    def tearDown(self):
        os.remove(tmpfile)

    def test_getip(self):
        self.assertEqual(xadmin.get_ip("emergency"), "911")
        self.assertEqual(xadmin.get_ip("peppes"), "22222222")
        
    def test_get_uri(self):
        self.assertEqual(xadmin.get_uri("booty"), "bootycall@jalla.com")

if __name__ == "__main__":
    unittest.main()