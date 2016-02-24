BioUtil
========

This is a collection of scripts and modules for bioinfomatics file access

Modules, Classes, and Functions
-------

xzFile, xzopen()
    access to various compressed files, currently recoganize gzip (.gz), 
    bz2(.bz2), and bgzip(.bgz, .b.gz) from samtools package

tsvFile, tsvRecord, tsv
    tab seperated file with named fields, user could also defined some preprocess
    functions for field reading and writing

vcfFile, vcf
    vcf file access, depends on `PyVCF <https://github.com/jamescasbon/PyVCF>`_,
    yet provide a convinient and flexable interface

samFile, sam
    sam file access, based on pysam_. 
    pysam_ also provides interface for tabix (random access tsv file with genome positions),
    which could be access from BioUtil.sam

    .. _pysam: https://github.com/pysam-developers/pysam

faidx
    interface to `pyfaidx <https://github.com/mdshw5/pyfaidx>`_

Dependency
------

- Python >= 3.4
- pysam >= 0.8.2
- PyVCF >= 0.6.7
- pyfaidx >= 0.4.7

Change Log
-------

v0.1.0
    inital release, support xzFile, tsvFile, vcfFile, samFile and faidx


Authors
--------
Yu XU

Lisense
--------
This module is under GPLv2 Lisense 


    

