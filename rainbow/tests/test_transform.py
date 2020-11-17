import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from transform import *
from conf import *

TestFile = "E:/develop/rainbow-git-latex/test/samplepaper.tex"
class TransformTest(unittest.TestCase):

    def test_load_commits(self):
        doc = Document()
        self.assertFalse(doc.active)
        
        doc.load(TestFile)

        self.assertTrue(doc.active)
        self.assertTrue(len(doc.commits)>0)

    def test_load_success(self):
        Len = 0

        doc = Document()
        doc.load(TestFile)
        with open(TestFile, "r", encoding="utf-8") as f:
            Len = len(f.readlines())
        
        self.assertEqual(len(doc.lines), Len)
        self.assertEqual(doc.file, TestFile)
        self.assertEqual(doc.path, "E:/develop/rainbow-git-latex/test")
        self.assertEqual(doc.outfile, os.path.join("E:/develop/rainbow-git-latex/test", "target/samplepaper.tex"))

    def test_load_error1(self):
        TestFile = "E:/develop/rainbow-git-latex/test/error1.tex"
        doc = Document()
        try:
            doc.load(TestFile)
        except TransformError:
            pass 
        else:
            assert False


    def test_load_error2(self):
        TestFile = "E:/develop/rainbow-git-latex/test/error1.tex"
        doc = Document()
        try:
            doc.load(TestFile)
        except TransformError:
            pass 
        else:
            assert False

    def test_mark(self):
        doc = Document()
        doc.load(TestFile)
        doc.mark()

        # something to test?

    def test_insert_color(self):
        doc = Document()
        doc.load(TestFile)
        doc.mark()
        doc.insert_colors()

        # something to test?

    def test_colorize(self):
        doc = Document()
        doc.load(TestFile)
        doc.mark()
        doc.colorize()

        # something to test?

    def test_output(self):
        doc = Document()
        doc.load(TestFile)
        doc.mark()
        doc.colorize()
        doc.output()

        self.assertTrue(os.path.exists(doc.outfile))

def main():
    unittest.main()