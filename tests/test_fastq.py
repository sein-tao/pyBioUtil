#!/usr/bin/env python3
import unittest
TestCase = unittest.TestCase
from BioUtil import fastqFile
import os

print("test fastqFile")
data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
def readfile(file):
    fh = open(file, 'r')
    content = fh.readlines()
    fh.close()
    return content

class TestFastq(TestCase):
    @classmethod
    def setUpClass(self):
        self.test_fa = os.path.join(data_dir, "test.fa")
        self.test_fq = os.path.join(data_dir, "test.fq")
        self.tmp_fa = os.path.join(data_dir, "tmp.fa")
        self.tmp_fq = os.path.join(data_dir, "tmp.fq")

    @classmethod
    def tearDownClass(self):
        os.remove(self.tmp_fa)
        os.remove(self.tmp_fq)

    def test_fasta(self):
        with fastqFile(self.tmp_fa, 'w') as out, fastqFile(self.test_fa) as input:
            for rec in  input:
                print(rec, file=out)
        gold_file = self.test_fa
        gold = readfile(gold_file)
        result = readfile(self.tmp_fa)
        self.assertEqual(gold, result)
    def test_fastq(self):
        with fastqFile(self.tmp_fq, 'w') as out, fastqFile(self.test_fq) as input:
            for rec in input:
                print(rec, file=out)
        gold = readfile(self.test_fq)
        result = readfile(self.tmp_fq)
        self.assertEqual(gold, result)



if __name__ == '__main__':
    unittest.main()


            
        

