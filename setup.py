#!/usr/bin/env python3

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='BioUtil',

        version='0.3.0',

        description='Bioinfomatics File access tools',
        long_description=long_description,

        # The project's main homepage.
        url='https://github.com/sein-tao/pyBioUtil',

        # Author details
        author='Yu XU',
        author_email='xuyu@genomics.cn',

        # Choose your license
        license='GPLv2',

        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering :: Bio-Informatics',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            ],

        # What does your project relate to?
        keywords='bioinfomatics sequencing fileIO',

        # You can just specify the packages manually here if your project is
        # simple. Or you can use find_packages().
        # packages=find_packages(exclude=['contrib', 'docs', 'tests']),
        packages = ['BioUtil'],

        install_requires=['pysam', 'PyVCF', 'pyfaidx', 'cython'],

)

