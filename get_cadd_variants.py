#!/usr/bin/env python
# encoding: utf-8
"""
get_cadd_variants.py

Remove all variants where CADD score < choosen treshold.

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
@click.option('--cadd_treshold', '-c',
                    default=15,
                    help="Set the treshold for cadd score. Default 15"
)
@click.option('-kw' ,'--keyword', 
                    default='CADD',
                    help="""Set the keyword for which info field that should be considered.
                            Default is 'CADD'"""
)
def get_cadd(variant_file, cadd_treshold, keyword):
    """Print only the rare variants to a new vcf"""
    cadd_treshold = float(cadd_treshold)
    if variant_file == '-':
        variant_parser = vcf_parser.VCFParser(fsock = sys.stdin)
    else:
        variant_parser = vcf_parser.VCFParser(infile = variant_file)
    nr_of_variants = 0
    for line in variant_parser.metadata.print_header():
        print(line)
    for variant in variant_parser:
        cadd_score = float(variant['info_dict'].get(keyword,'0'))
        if cadd_score >= cadd_treshold:
            print('\t'.join([variant[entry] for entry in variant_parser.metadata.header]))
    
if __name__ == '__main__':
    get_cadd()