#!/usr/bin/env python
# encoding: utf-8
"""
get_covered_variants.py

Remove all variants where not all individuals are covered to a certain depth.

Created by Måns Magnusson on 2014-04-30.
Copyright (c) 2014 __MoonsoInc__. All rights reserved.
"""

from __future__ import print_function
from __future__ import unicode_literals


import sys
import os
import click

from vcf_parser import parser as vcf_parser
from codecs import getwriter

if sys.version_info < (3,0):
    sys.stdout = getwriter('UTF-8')(sys.stdout)


@click.command()
@click.argument('variant_file', 
                    nargs=1, 
                    type=click.Path(exists=True),
                    metavar='<vcf_file>'
)
@click.option('--rare', '-rare',
                    default=0.05,
                    help="Set the treshold for rare variants. Default 0.05"
)
@click.option('-kw' ,'--keyword', 
                    default='AF',
                    help="""Set the keyword for which info field that should be considered.
                            Default is 'AF'"""
)
def get_rare(variant_file, rare, keyword):
    """Print only the rare variants to a new vcf"""
    
    if variant_file == '-':
        variant_parser = vcf_parser.VCFParser(fsock = sys.stdin)
    else:
        variant_parser = vcf_parser.VCFParser(infile = variant_file)
    nr_of_variants = 0
    for line in variant_parser.metadata.print_header():
        print(line)
    for variant in variant_parser:
        interesting = True
        maf = [float(allele) for allele in variant['info_dict'].get(keyword,'0').split(',')]
        if min(maf) < rare:
            print('\t'.join([variant[entry] for entry in variant_parser.metadata.header]))
    
if __name__ == '__main__':
    get_rare()