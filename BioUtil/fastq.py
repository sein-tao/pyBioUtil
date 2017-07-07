#!/usr/bin/env python3
"""fasta/fastq file IO"""
from .readfq import readfq
from .xz import xzFile, xzopen
import textwrap
from itertools import starmap

__all__ = [ 'fastqRecord', 'fastqFile', 'fastaRecord', 'fastaFile',
        'fastqReader', 'fastqWriter']

class fastqRecord:
    """a fastq/fasta Record.
    Attibutes: name, seq, qual"""
    def __init__(self, name, seq, qual=None):
        self.name = name
        self.seq = seq
        self.qual = qual
    @property
    def isfa(self):
        "boolean, True for fasta, False for fastq"
        return self.qual is None

    def to_str(self, linewidth=None):
        """covert record to string, without newline character on last line
        linewidth only affect the output of fasta"""
        if self.isfa:
            header = '>%s\n' % self.name
            if linewidth is None:
                seq = self.seq
            else:
                seq = textwrap.fill(self.seq, linewidth)
            return header + seq
        else:
            return "@{name}\n{seq}\n+\n{qual}".format_map(self.__dict__)

    def __str__(self):
        return self.to_str()

    def __len__(self):
        "get length of seq"
        return len(self.seq)

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
    def __init__(self, file, mode='w', linewidth=None):
        """init writer. linewidth only affect fa records, set to None mean one line"""
        super(self.__class__, self).__init__(file, mode)
        self.linewidth = linewidth

    def __enter__(self):
        return self

    def write(self, rec):
        "write record, automately ends with newline"
        if isinstance(rec, str): # for print
            self.fh.write(rec)
        elif isinstance(rec, fastqRecord):
            self.fh.write(rec.to_str(self.linewidth))
            self.fh.write("\n")
        else:
            raise TypeError("%s for fastqWriter" % type(rec))


class fastqFile:
    """ fasta/fastq file IO """
    def __new__(cls, file, mode='r', linewidth=None, *args, **kwargs):
        "construct fastqFile for I/O"
        if 'r' in mode:
            return fastqReader(file, mode, *args, **kwargs)
        elif 'w' in mode:
            return fastqWriter(file, mode, linewidth, *args, **kwargs)
        else:
            raise ValueError("Invalid mode: %s" % mode)

fastaFile = fastqFile
fastaRecord = fastqRecord
