#!/usr/bin/env python3
"""fasta/fastq file IO"""
from readfq import readfq
from xz import xzopen
import textwrap

default_linewidth = 70
class fastqRecord:
    def __init__(self, name, seq, qual=None):
        self.name = name
        self.seq = seq
        self.qual = qual
    @property
    def isfa(self):
        return self.qual is None

    def __str__(self):
        if self.isfa:
            header = '>%s\n' % self.name
            seq = textwrap.fill(self.seq, default_linewidth)
            return header + seq + "\n"
        else:
            return "@{name}\n{seq}\n+\n{qual}\n".format(self.__dict__)

class fastqReader:
    """ fasta/fastq file IO 
        use readfq.py by lh3
    """

    def __init__(self, file, mode='r'):
        self.file = file
        self.fh = xz.open(file, mode)
        self.iter = readfq(self.fh)

    def close(self):
        return self.fh.close()

    def __iter__(self):
        return self.iter

    def __next__(self):
        return next(self.iter)

    def __enter__(self):
        return self

    def __exit__(self, exc, val, trace):
        self.close()


class fastqWriter:
    """ fasta/fastq file IO """
    def __new__(cls, file, mode='w'):
        return xzopen(file, mode)

class fastqFile:
    def __new__(cls, file, mode='r'):
        if 'r' in mode:
            return fastqReader(file, mode)
        elif 'w' in mode:
            return fastqWriter(file, mode)
        else:
            raise ValueError("Invalid mode: %s" % mode)

