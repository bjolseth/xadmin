#!/usr/bin/env python3

import unittest
import os
import subprocess

import xadmin

sampledata = """
911          emergency    emergency@nowhere.com

22222222     peppes       pizza@peppes.com
10.54.80.30  sx20         tbjolset.sx20@lys.cisco.com
1234         booty        bootycall@jalla.com
"""

tmpfile = "testdata.txt"

class TestXadmin(unittest.TestCase):

    def setUp(self):
        with open(tmpfile, 'w') as file:
            file.write(sampledata)

        os.environ['XADMIN_FILE'] = tmpfile
        os.environ['XADMIN_DRY'] = "1"
        
    def tearDown(self):
        os.remove(tmpfile)
        os.unsetenv('XADMIN_FILE')
        os.unsetenv('XADMIN_DRY')

    def run_cmd(self, cmd):
        result = subprocess.check_output(cmd, shell=True)
        return result.decode("utf-8").strip()
        

    def test_xadmin(self):
        output = self.run_cmd("./xadmin.py --admin emergency")
        self.assertEqual(output, "ssh admin@911")

        output = self.run_cmd("./xadmin.py --admin booty")
        self.assertEqual(output, "ssh admin@1234")

        output = self.run_cmd("./xadmin.py --admin ")
        self.assertEqual(output, "ssh admin@10.54.80.30")
        
    def test_xroot(self):
        output = self.run_cmd("./xadmin.py --root peppes")
        self.assertEqual(output, "ssh root@22222222")
        
        output = self.run_cmd("./xadmin.py --root ")
        self.assertEqual(output, "ssh root@10.54.80.30")

    def test_dial(self):
        output = self.run_cmd("./xadmin.py --dial")
        self.assertEqual(output, "echo 'xcommand dial number: tbjolset.ex90@lys.cisco.com' | ssh admin@10.54.80.30 /bin/tsh")

        output = self.run_cmd("./xadmin.py --dial jalla@jalla")
        self.assertEqual(output, "echo 'xcommand dial number: jalla@jalla' | ssh admin@10.54.80.30 /bin/tsh")

        output = self.run_cmd("./xadmin.py --dial peppes")
        self.assertEqual(output, "echo 'xcommand dial number: pizza@peppes.com' | ssh admin@10.54.80.30 /bin/tsh")

        output = self.run_cmd("./xadmin.py --dial peppes booty")
        self.assertEqual(output, "echo 'xcommand dial number: pizza@peppes.com' | ssh admin@1234 /bin/tsh")
        
    def test_answer(self):
        output = self.run_cmd("./xadmin.py --answer")
        self.assertEqual(output, "echo 'xcommand call accept' | ssh admin@10.54.80.30 /bin/tsh")

        output = self.run_cmd("./xadmin.py --answer peppes")
        self.assertEqual(output, "echo 'xcommand call accept' | ssh admin@22222222 /bin/tsh")
    
    def test_disconnect(self):
        output = self.run_cmd("./xadmin.py --disconnect")
        self.assertEqual(output, "echo 'xcommand call disconnectall' | ssh admin@10.54.80.30 /bin/tsh")

        output = self.run_cmd("./xadmin.py --disconnect peppes")
        self.assertEqual(output, "echo 'xcommand call disconnectall' | ssh admin@22222222 /bin/tsh")

    def test_pair(self):
        output = self.run_cmd("./xadmin.py --pair")
        self.assertEqual(output, "adb shell am broadcast -a com.cisco.CODEC_CONFIG_UPDATED -e address 10.54.80.30 -e username admin -e password ''")

        output = self.run_cmd("./xadmin.py --pair booty")
        self.assertEqual(output, "adb shell am broadcast -a com.cisco.CODEC_CONFIG_UPDATED -e address 1234 -e username admin -e password ''")

    def test_search(self):
        output = self.run_cmd("./xadmin.py --search jalla").split("\n")
        self.assertEqual(output[0], "echo 'xstatus' | ssh admin@10.54.80.30 /bin/tsh | grep -i jalla")
        self.assertEqual(output[1], "echo 'xconfig' | ssh admin@10.54.80.30 /bin/tsh | grep -i jalla")

        output = self.run_cmd("./xadmin.py --search jalla emergency").split("\n")
        self.assertEqual(output[0], "echo 'xstatus' | ssh admin@911 /bin/tsh | grep -i jalla")
        self.assertEqual(output[1], "echo 'xconfig' | ssh admin@911 /bin/tsh | grep -i jalla")

    def test_web(self):
        output = self.run_cmd("./xadmin.py --web")
        self.assertEqual(output, "google-chrome  http://10.54.80.30")

        output = self.run_cmd("./xadmin.py --web booty")
        self.assertEqual(output, "google-chrome  http://1234")

    def test_getip(self):
        self.assertEqual(xadmin.get_ip("emergency"), "911")
        self.assertEqual(xadmin.get_ip("peppes"), "22222222")
        
    def test_get_uri(self):
        self.assertEqual(xadmin.get_uri("booty"), "bootycall@jalla.com")

if __name__ == "__main__":
    unittest.main()