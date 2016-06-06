#!/usr/bin/env python3
"""fasta file access with buffer"""
import pysam

class cachedFasta:
    """fasta seq fetcher, use buffer to improve performance
        example: 
        fa = cachedFasta("hg19.fa")
        seq = fa['chr1'][2000:3000] 
    """

    def __init__(self, fa, trans=None, buffer_size = ('-2k', '8k') ):
        """ fa: fasta file name, or pysam.FastaFile object
                fa file could be either text file or bgzip-ed (gzipped is *NOT OK*)
                if file name is provide, filename.fai chould be provoide or
                it will automately build by samtools faidx
            trans: transform function before sequence return, no transform by default
                eg. trans = str.upper if change seq to uppercase
            buffer_size: tuple, left(negative) and right (positive) buffer size,
                relative to buffer allocate query position
                support both integer or number with suffix k,M
        """
        if not isinstance(fa, pysam.FastaFile):
            fa = pysam.FastaFile(fa)
        self.fa = fa
        self.ref_len = dict(zip(fa.references, fa.lengths))
        self.buffer_size = buffer_size
        self.__set_trans(trans)
        # self.buffer_size = tuple(map(readable2num, buffer_size))
        # self.buffer = _seqBuffer(self.fa, self.buffer_size)

    @property
    def buffer_size(self):
        """ seq buffer size, relative to buffer allocate query position
        get the value will return a tuple (left buffer size, right buffer size),
        where left size is a negative number
        when set the value, use the tuple with the same format, while each size
        support both integer or number with suffix k,M
        """
        return self.__buffer_size
    
    @buffer_size.setter
    def buffer_size(self, size_tuple):
        self.__buffer_size = tuple(map(readable2num, size_tuple)) 
        self.buffer = _seqBuffer(self.fa, self.buffer_size)

    @property
    def trans(self):
        "transform function" # , set to None to disable transform"
        return self.__trans

    # @trans.setter
    def __set_trans(self, func):
        if func is None:
            func = lambda x : x
        self.__trans = func



    def __getitem__(self, chr):
        """ select chr, by chr name or chr index number
        return chrFetcher object, from which seq could be accessed by slicing
        """
        if isinstance(chr, int):
            chr = self.fa.references[chr]
        if chr not in self.ref_len:
            raise KeyError("reference %s not found." % chr)
        else:
            return _chrFetcher(self, chr) 
    def fetch(self, chr, start, end):
        return self[chr][start:end]
    def fetch_entry(self, chr):
        return self[chr][:]

    def close(self):
        self.fa.close()


class _chrFetcher:
    "fetch seq on one reference"
    def __init__(self, genome, chr):
        self.database = genome
        self.chr = chr
        self.chr_len = genome.ref_len[chr]
        self.buffer = genome.buffer
        self.trans = genome.trans
    def __getitem__(self, key):
        "get seq, start and stop are 0-based, stop exclusive"
        # print(key)
        if isinstance(key, int):
            if key >= self.chr_len or key < - self.chr_len:
                raise IndexError("index out of range: %s:%s"
                        % (chr, key))
            key = slice(key, key+1)
        if not isinstance(key, slice):
            raise TypeError("Unkonwn index type")
        key = slice(*key.indices(self.chr_len))
        if not (self.chr == self.buffer.chr and 
                key.start >= self.buffer.start and  
                key.stop <= self.buffer.end):
            self.buffer.fetch(self.chr, key.start, key.stop)
        return self.trans(self.buffer[key])
    def fetch(self, start, end):
        return self[start:end]

class _seqBuffer:
    def __init__(self, fa, buffer_size):
        self.fa = fa
        self.left, self.right = buffer_size
        self.chr = None
    def __getitem__(self, key):
        start0 = key.start - self.start
        stop0 = key.stop - self.start
        return self.seq[slice(start0,stop0, key.step)]
    def fetch(self, chr, start, stop):
        chr_len = self.fa.get_reference_length(chr)
        self.chr = chr
        self.start = max(0, start + self.left)
        self.end = min(stop + self.right, chr_len)
        self.seq = self.fa.fetch(self.chr, self.start, self.end)


def readable2num(length):
    "convert readable number (with suffix) to integer"
    if isinstance(length, int):
        return length
    elif isinstance(length, str):
        suffix = length[-1]
        if suffix.isdigit():
            return int(length)
        else:
            if suffix in ('K', 'k'):
                base = 1000
            elif suffix in ('M', 'm'):
                base = 1e6
            else:
                raise ValueError(length)
            pre = float(length[:-1])
            return round(pre * base)
    else:
        raise ValueError(length)

