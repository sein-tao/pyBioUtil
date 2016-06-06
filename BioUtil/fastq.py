#!/usr/bin/env python3
"""fasta/fastq file IO"""
from .readfq import readfq
from .xz import xzFile, xzopen
import textwrap
from itertools import starmap

__all__ = [ 'fastqRecord', 'fastqFile', 'fastaRecord', 'fastaFile',
        'default_linewidth']

default_linewidth = 70
class fastqRecord:
    def __init__(self, name, seq, qual=None):
        self.name = name
        self.seq = seq
        self.qual = qual
    @property
    def isfa(self):
        return self.qual is None

    def to_str(self, linewidth=default_linewidth):
        if self.isfa:
            header = '>%s\n' % self.name
            seq = textwrap.fill(self.seq, linewidth)
            return header + seq
        else:
            return "@{name}\n{seq}\n+\n{qual}".format_map(self.__dict__)

    def __str__(self):
        return self.to_str()

class fastqReader:
    """ fasta/fastq file reader 
        use readfq.py by lh3
    """

    def __init__(self, file, mode='r'):
        self.file = file
        self.fh = xzopen(file, mode)
        self.iter = starmap(fastqRecord, readfq(self.fh))

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


class fastqWriter (xzFile):
    """ fasta/fastq file writer """
    def __init__(self, file, mode='w', linewidth=default_linewidth):
        super(self.__class__, self).__init__(file, mode)
        self.linewidth = linewidth

    def write(self, rec):
        if not isinstance(rec, fastqRecord):
            raise TypeError()
        super(self.__class__, self).write(rec.to_str(self.linewidth))


class fastqFile:
    """ fasta/fastq file IO """
    def __new__(cls, file, mode='r', *args, **kwargs):
        if 'r' in mode:
            return fastqReader(file, mode, *args, **kwargs)
        elif 'w' in mode:
            return fastqWriter(file, mode, *args, **kwargs)
        else:
            raise ValueError("Invalid mode: %s" % mode)

fastaFile = fastqFile
fastaRecord = fastqRecord
