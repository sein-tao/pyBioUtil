#!/usr/bin/env python3
import unittest
TestCase = unittest.TestCase
from BioUtil.fasta import fastaReader
import pysam
import os
import logging
logging.basicConfig(level=logging.ERROR)

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
test_file = os.path.join(data_dir, "test.fasta")
class TestFastaFileInit(TestCase):
    def setUp(self):
        self.files = ["test.fasta", "test.fa", "test.fa.gz", "test.fa.b.gz", "hg19.fa"]

    def test_open(self):
        for file in self.files:
            file = os.path.join(data_dir, file)
            logging.info("test file %s" % file)
            if (os.path.exists(file) and
                    not (file.endswith(".gz") and not file.endswith(".b.gz")) ): 
                    # and os.path.exists(file + ".fai"):
                self.assertIsInstance(fastaReader(file), fastaReader)
            else:
                self.assertRaises(OSError, fastaReader, file)

class TestFastaFileFetch(TestCase):
    def setUp(self):
        self.fa = fastaReader(test_file)
        self.ref = pysam.FastaFile(test_file)

    def test_chr(self):
        test_chrs = ['1', 'chr1', '4', 'abc', 'Long seq']
        for chr in test_chrs:
            try:
                seq = self.ref.fetch(chr)
            except KeyError:
                self.assertRaises(KeyError, self.fa.__getitem__, chr)
            else:
                self.assertEqual(self.fa[chr][:], seq)
    def test_chr_byindex(self):
        test_chrs = [-1, 1, 5, 10, 2000]
        for chr in test_chrs:
            logging.info("test chr index %s" % chr)
            try:
                # pysam.FastaFile does not support access by index, bypass it
                seq = self.ref.fetch(self.ref.references[chr])
            except LookupError:
                self.assertRaises(IndexError, self.fa.__getitem__, chr)
            else:
                self.assertEqual(seq, self.fa[chr][:])

    def test_position_fetch(self):
        # pysam.FastaFile use space as seqname seperator, remove the space
        # logging.info(self.ref.references)
        # chr = "Long seq"
        chr = "LongSeq"
        L = self.ref.get_reference_length(chr)
        q1, q2, q3 = [int(i/4 * L) for i in range(1,4)]
        self.assertEqual(self.fa[chr][q1:q2], self.ref.fetch(chr, q1, q2) )
        self.assertEqual(self.fa[chr][:q2], self.ref.fetch(chr, end = q2) )
        self.assertEqual(self.fa[chr][q2:], self.ref.fetch(chr, start=q2))
        self.assertEqual(self.fa[chr][:], self.ref.fetch(chr) )
        self.assertEqual(self.fa[chr][q2], self.ref.fetch(chr)[q2] )
        self.assertEqual(self.fa[chr][-q2], self.ref.fetch(chr)[-q2] )
        self.assertRaises(TypeError, self.fa[chr].__getitem__, q2 + 0.5)
        self.assertEqual(self.fa[chr][q3:L+1], self.ref.fetch(chr, q3, L+1))
        self.assertRaises(IndexError, self.fa[chr].__getitem__, L + 1)


class TestFastaFileTrans(TestCase):
    def test_trans(self):
        self.raw = fastaReader(test_file, trans=None)
        chr = "LongSeq"
        region = slice(0,15)
        upper = fastaReader(test_file, trans = str.upper)
        self.assertEqual(upper[chr][region], self.raw[chr][region].upper())
        rev = fastaReader(test_file, trans = lambda x: x[::-1])
        self.assertEqual(rev[chr][region], self.raw[chr][region][::-1])


   

                




if __name__ == '__main__':
    unittest.main()
