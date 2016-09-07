#!/usr/bin/env python3
"""
This module serves as a wrapper for vcf module [https://github.com/jamescasbon/PyVCF]
open() and vcfFile class is for directly init of vcf file object,
vcfReader and vcfWriter is wraper for vcf.Reader and vcf.Writer,
which accept file name as first argument (other than fsock), 
and also could accept vcf file without header (by additionally provide header infomation)

This file is under GPLv2 Lisense

Sein Tao <sein.tao@gmail.com>, 2015
"""

import vcf
import csv
import types
import os
import builtins
from .xz import xzopen
from itertools import chain
from copy import copy, deepcopy
from .decorator import context_decorator
# import log
# log.basicConfig(level=log.DEBUG)

__all__ = ['vcfFile', 'open', 'vcfWriter', 'vcfReader']

_vcf = vcf
_Reader = vcf.Reader
_Writer = vcf.Writer
Record=vcf.model._Record
Call=vcf.model._Call



class vcfFile(object):
    def __new__(cls, file, mode='r', template=None, prepend_chr=False):
        if mode == 'r':
            # add filename to avoid the **stupid** compression detection on stream from vcf module
            obj = vcf.Reader(xzopen(file, mode), prepend_chr=prepend_chr, filename=file)
            obj.close = types.MethodType(lambda self: self._reader.close(), obj)
            return obj
        elif mode == 'w':
            obj = vcf.Writer(xzopen(file, mode), template)
            obj.write = obj.write_record
            return obj
        else:
            raise ValueError("Unkonw mode: " + mode)

def _read_header(self, header, template):
    if header and template:
        raise ValueError("only one of header and template should specified")
    if header:
        header_fh = xzopen(header, 'r')
        template = vcf.Reader(header_fh)
        header_fh.close()
    return template

@context_decorator
class vcfReader(vcf.Reader):
    def __init__(self, file=None, header=None, fsock=None, 
             template=None,  **kwargs):
        if fsock:
            self._fsock = fsock
        elif file:
            self._fsock = xzopen(file, 'r')
        template = _read_header(self, header, template)
        sup = super(self.__class__, self)
        if template:
            self._parse_metainfo = types.MethodType(lambda self: None, self)
            sup.__init__(self._fsock, filename=file, **kwargs)
            for attr in ('metadata', 
                    'infos', 'filters', 'alts', 'contigs', 'formats',
                    '_column_headers', 'samples', '_sample_indexes'):
                setattr(self, attr, deepcopy(getattr(template, attr)) )
        else:
            sup.__init__(self._fsock, filename=file, **kwargs)

    def close(self):
        try:
            self._fsock.close()
        except AttributeError:
            pass


@context_decorator
class vcfWriter(vcf.Writer):
    def __init__(self, file=None, header=None, fsock=None, 
             template=None, write_header = True, **kwargs):
        template = _read_header(self, header, template)
        if fsock:
            self._fsock = fsock
        elif file:
            self._fsock = xzopen(file, 'w')
        sup = super(self.__class__, self)
        if  write_header is False:
            null = builtins.open(os.devnull, 'w')
            sup.__init__(null, template, **kwargs)
            null.close()
            self.stream = self._fsock
            self.writer = csv.writer(self.stream, delimiter="\t", 
                    lineterminator=kwargs.get("lineterminator","\n"))
        else:
            sup.__init__(self._fsock, template, **kwargs)

        self.write = self.write_record


def open(file, mode='r', header = None, **kwargs):
    "wrapper for vcfReader and vcfWriter"
    #D# log.debug([mode, kwargs])
    if 'r' in mode:
        return vcfReader(file, header=header, **kwargs)
    elif 'w' in mode:
        return vcfWriter(file, header=header, **kwargs)
    else:
        raise ValueError("unknown mode: %s" % mode)





