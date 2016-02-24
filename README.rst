BioUtil
========

This is a collection of scripts and modules for bioinfomatics file access

General file access
-------

xzopen.py
    access to various compressed files, currently recoganize gzip (.gz), 
    bz2(.bz2), and bgzip(.bgz, .b.gz) from samtools package

tsv.py
    tab seperated file with named fields, user could also defined some preprocess
    functions for field reading and writing

Formatted file access
--------

vcf file
    pyvcf module, which depends on `vcf module<https://github.com/jamescasbon/PyVCF>`_,
    yet provide a more convinient interface

sam file
    `pysam module<https://github.com/pysam-developers/pysam>`. This module
    also provides interface for tabix (random access tsv file with genome positions)

fasta file
    `pyfaidx module<https://github.com/mdshw5/pyfaidx>`

Dependency
------

- Python >= 3.4
- pysam >= 0.8.2
- vcf >= 0.6.7
- pyfaidx >= 0.4.7

Authors
--------
Yu XU, xuyu@genomics.cn

Lisense
--------
This module is under GPLv2 Lisense 


    

