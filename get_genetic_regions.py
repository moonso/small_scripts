#!/usr/bin/env python
# encoding: utf-8
"""
get_genetic_regions.py

get variants based on their genetic regions.

Created by Måns Magnusson on 2013-04-09.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

from __future__ import division
from __future__ import unicode_literals


import sys
import os
import click

import click
# import prettyplotlib as ppl
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from codecs import open

from vcf_parser import parser as vcf_parser


from datetime import datetime
from pprint import pprint as pp


@click.command()
@click.argument('variant_file', 
                    nargs=1, 
                    type=click.Path(exists=True),
                    metavar='<vcf_file>'
)
@click.argument('outfile', 
                    nargs=1, 
                    type=click.Path(exists=False),
)
@click.option('-gene' ,'--gene', 
                    is_flag=True,
                    help='If only genetic variants should be considered.'
)
@click.option('-rare' ,'--rare', 
                    is_flag=True,
                    help='If only rare variants should be considered.'
)

def get_genetic_region(variant_file, outfile, gene, rare):
    """check the variants"""
    variant_parser = vcf_parser.VCFParser(variant_file)
    regions = {}
    current_features = []
    beginning = True
    new_chrom = None
    current_chrom = None
    
    outfile = open(outfile, mode='w', encoding='utf-8', errors='replace')
    
    nr_of_variants = 0
    variants_in_region = 0
    
    start_twenty_time = datetime.now()
    start_time = datetime.now()
    
    region_count = 1
    
    all_genes = set()
    cadd_scores = []
    
    for variant in variant_parser:
        
        cadd_score = float(variant['info_dict'].get('CADD', '0'))
        cadd_scores.append(cadd_score)
        new_chrom = variant['CHROM']
        position = variant['POS']
        nr_of_variants += 1
        new_features = variant['info_dict'].get('Annotation', '')
        all_genes = (all_genes | set(new_features.split(',')))
        
        
        if beginning:
            current_features = new_features
            beginning = False
            # Add the variant to each of its features in a batch
            current_chrom = new_chrom
        else:
            
            send = True
            # print(current_features, new_features)
            
            if len(new_features) == 0:
                if len(current_features) == 0:
                    send = False
            
            #If not check if we are in a region with overlapping genes
            
            elif len(set.intersection(set(new_features.split(',')),set(current_features.split(',')))) > 0:
                send = False
            
            if new_chrom != current_chrom:
                # New chromosome means new batch
                send = True
                current_chrom = new_chrom
                
            if send:
                
                if not len(current_features) == 0:
                    # print(current_features, len(cadd_scores))
                    regions[region_count] = (variants_in_region, position, current_features, new_features)
                    for cadd_score in cadd_scores:
                        # if int(cadd_score) > 10:
                        #     print(cadd_score)
                        outfile.write(str(region_count) + '\t' + str(cadd_score) + '\n')
                        cadd_scores = []
                    region_count += 1
                variants_in_region = 0
                current_features = new_features
            else:
                current_features = ','.join(list(set(current_features.split(',')) | set(new_features.split(','))))
                variants_in_region += 1
                
    if len(current_features) > 0:
        regions[region_count] = (variants_in_region, position, current_features, new_features)
    pp(regions)
    print('All genes: %s' % str(all_genes))
    print('Time for analysis: %s' % str(datetime.now() - start_time))
            

if __name__ == '__main__':
    get_genetic_region()