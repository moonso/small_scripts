#!/usr/bin/env python
# encoding: utf-8
"""
get_covered_variants.py

Remove all variants where not all individuals are covered to a certain depth or have a certain genotype quality.

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
from datetime import datetime
from pprint import pprint as pp

if sys.version_info < (3,0):
    sys.stdout = getwriter('UTF-8')(sys.stdout)


@click.command()
@click.argument('variant_file', 
                    nargs=1, 
                    type=click.Path(exists=True),
                    metavar="<vcf_file> or '-'"
)
@click.option('-depth' ,'--depth',
                    default=7,
                    help='Specify the depth that all individuals should have. Default 7'
)
@click.option('-gq' ,'--genotype_quality',
                    type=float,
                    help='Specify the minimum genotype quality for variant to be considered. Default 20'
)
def get_covered(variant_file, depth, genotype_quality):
    """Print the variants that are covered to a certain depth(or have a certain genotype quality) to a new vcf.
        If no parameters given all variants with read depth > 7 in all individuals will be choosen."""
    
    if variant_file == '-':
        variant_parser = vcf_parser.VCFParser(fsock = sys.stdin)
    else:
        variant_parser = vcf_parser.VCFParser(infile = variant_file)
    
    nr_of_variants = 0
        
    for line in variant_parser.metadata.print_header():
        print(line)
    
    for variant in variant_parser:
        interesting = True
        genotypes = variant.get('genotypes', {})
        for individual in genotypes:
            if genotype_quality:
                if genotypes[individual].genotype_quality < genotype_quality:
                    interesting = False
            else:
                #If any individual has depth below "depth" we do not consider the variant
                if genotypes[individual].quality_depth < depth:
                    interesting = False
        if interesting:
            print('\t'.join([variant[entry] for entry in variant_parser.metadata.header]))
    
if __name__ == '__main__':
    get_covered()