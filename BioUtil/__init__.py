from pkg_resources import get_distribution
__version__ =  get_distribution('BioUtil').version
__all__ = ['xzopen', 'tsv', 'vcf', 'vcfFile', 'sam', 'samFile', 'faidx']

from xzopen import xzopen
import tsv
import pyvcf as vcf
import pysam as sam
import pyfaidx as faidx
from pyvcf import vcfFile
from pysam import AlignmentFile as samFile


