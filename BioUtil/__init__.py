from pkg_resources import get_distribution
__version__ =  get_distribution('BioUtil').version
__all__ = ['xzFile', 'xzopen', 
        'tsv', 'tsvFile', 'tsvRecord',
        'vcf', 'vcfFile', 'vcfReader', 'vcfWriter', 
        'samFile', 
        'fastaFile', 'fastqFile', 'fastaRecord', 'FastqRecord',
        'cachedFasta', 'faidx',
        ]
# the order matters to avoid loop
from .xz import xzFile, xzopen
# from . import xz

from .tsv import tsvFile, tsvRecord
# from . import tsv

from .vcf import vcfFile, vcfReader, vcfWriter, _vcf
# from . import vcf

from pysam import AlignmentFile as samFile
import pysam as sam

from .cached_fasta import cachedFasta
fastaReader=cachedFasta

from .fastq import fastqFile, fastqRecord, fastaFile, fastaRecord

import pyfaidx as faidx

