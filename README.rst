BioUtil
========

This is a collection of scripts and modules for bioinfomatics file access

Modules, Classes, and Functions
---------------------------------

xzFile, xzopen()
    access to various compressed files, currently recoganize gzip (.gz), 
    bz2(.bz2), and bgzip(.bgz, .b.gz) from samtools package

tsvFile, tsvRecord, tsv
    tab seperated file with named fields, user could also defined some preprocess
    functions for field reading and writing

vcfFile, vcf
    vcf file access, depends on PyVCF_,
    yet provide a convinient and flexable interface

samFile, sam
    sam file access, based on pysam_. 
    pysam_ also provides interface for tabix (random access tsv file with genome positions),
    which could be access from BioUtil.sam

fastqFile, fastaFile:
    fasta/fastq file IO. based on lh3 readfq_.

cachedFasta
    fetch region sequence from large fasta file. This module is based on faidx 
    through pysam_ pysam.FastaFile.
    *from v0.1.2*: old name fastaReader is deprecated as misleading with fastaFile reader

faidx
    experimental, interface to pyfaidx_.

Dependency
------------

- Python >= 3.4
- pysam_ >= 0.8.2
- PyVCF_ >= 0.6.7
- pyfaidx_ >= 0.4.7

Change Log
-------------

v0.2
    add fastqFile, rename fastaReader to cachedFasta

v0.1.1
    add fastaReader

v0.1.0
    inital release, support xzFile, tsvFile, vcfFile, samFile and faidx


Authors
--------
Yu XU

Lisense
--------
This module is under GPLv2 Lisense 

    
.. _pysam: https://github.com/pysam-developers/pysam
.. _PyVCF: https://github.com/jamescasbon/PyVCF
.. _pyfaidx: https://github.com/mdshw5/pyfaidx
.. _readfq: https://github.com/lh3/readfq

