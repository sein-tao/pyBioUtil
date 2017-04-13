#!/usr/bin/env python
"""
This module defines the base classes of tsv file (with named fields).  
tsvFile is the base class for tsv file, 
and tsvRecord is the base class for tsv record.
the subclasses of tsvFile should specify the Record attribute, 
which is typically a tsvRecord subclass.
To define a subclass of tsvRecord, you at least to specifiy _fields,
the attribute names for Record columns.

Example:
import tsv
class bedFile(tsv.tsvFile):
    class Record(tsv.tsvRecord):
        _fields = ("chr", "start", "end")


AUTHOR	Sein Tao, <sein.tao@gmail.com>
VERSION	0.1
2015-05-18 10:43:54 CST
"""

from .xz import xzopen
# from collections import OrderedDict, namedtuple
from copy import copy, deepcopy
import shlex
__all__ = ['tsvFile', 'tsvRecord', '_read_sha_header', '_write_sha_header']

class tsvFile(object):
    Record = None
    def __init__(self, file, mode='r', template=None): 
        self.filename = file
        if mode in ('r','w'):
            self.mode = mode
        else:
            raise ValueError("Unkown mode: %s" % mode)
        self._fh = xzopen(file, mode)
        self.meta = None
        self.header = None
        if mode == 'r':
            self._read_header()
        if template is not None:
            self.meta = deepcopy(template.meta)
            self.header = deepcopy(template.header)
        if mode == 'w':
            self._write_header()
    
    @classmethod
    def open(cls, file, mode='r', template=None):
        return cls(file, mode, template)

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc, val, trace):
        self.close()

    def __next__(self):
        "read the next record"
        return self.Record(next(self._fh).rstrip("\n").split("\t"))

    def write(self, record):
        "write a record"
        self._fh.write(record.to_str())
        self._fh.write("\n")

    def _read_header(self):
        pass

    def _write_header(self):
        pass

    def close(self):
        return self._fh.close()

class tsvRecord(object):
    _fields = tuple()
    _fields_parser = dict()
    _fields_encoder= dict()
    _fields_default= dict()

    def __init__(self, rec):
        cls = self.__class__
        if rec is None:
            pass
        elif isinstance(rec, list) or isinstance(rec, tuple):
            parser = lambda k: cls._fields_parser.get(k, lambda x:x)
            if len(rec) != len(cls._fields):
                raise ValueError("field number not match (%s provide, %s needed). " %(len(rec), len(cls._fields)) + 
                        "line:\n" + "\t".join(map(shlex.quote, rec)) )
            for i, k in enumerate(cls._fields):
                setattr(self, k, parser(k)(rec[i]) )
        elif isinstance(rec, dict):
            for k, v in rec.iteritems():
                setattr(self, k, v)
        elif isinstance(rec, tsvRecord):
            for k in set(rec._fields).intersect(set(cls._fileds)):
                setattr(self, k, rec.k)
        else:
            raise ValueError("Unknown argument type")
    def to_str(self):
        return "\t".join(self._fields_encoder.get(attr,str)(getattr(self, attr)) 
                for attr in self._fields)

    def __getattr__(self, attr):
        try:
            return  self._fields_default[attr]
        except KeyError:
            raise AttributeError("Attribute %s not exist." % attr)


def _read_sha_header(self):
    """read vcf-file like header. 
    (meta lines starts with ##, header line start with #, no blanklines between).
    """
    self.meta = list()
    has_header = None
    while True:
        line = next(self._fh)
        if has_header is None:
            has_header = line.startswith('##')
            if not has_header:
                raise ValueError("inputfile does not have header")
        if line.startswith('##'):
            self.meta.append(line)
        elif line.startswith("#"):
            self.header = line
            break
    return

def _write_sha_header(self):
    "write vcf-file like header."
    if self.header:
        for line in self.meta:
            self._fh.write(line)
        self._fh.write(self.header)
    return



