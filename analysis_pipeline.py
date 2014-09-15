#!/usr/bin/env python
# encoding: utf-8
"""
analysis_pipeline.py

Make an analysis pipeline based on the existing paths on rasta.

Created by Måns Magnusson on 2014-04-30.
Copyright (c) 2014 __MoonsoInc__. All rights reserved.
"""

from __future__ import print_function
from __future__ import unicode_literals


import sys
import os
import click
import yaml

from vcf_parser import parser as vcf_parser
from codecs import getwriter, open

if sys.version_info < (3,0):
    sys.stdout = getwriter('UTF-8')(sys.stdout)

from pprint import pprint as pp

BASE_PATH = '/mnt/hds/proj/cust003/'

REF_DIR = 'mip_references'
THOUSAND_G = 'ALL.autosomes.phase3_shapeit2_mvncall_integrated_v3.20130502.sites.vcf.gz'


@click.command()
@click.argument('family', 
                    nargs=1, 
                    type=str,
                    metavar='<family_to_be_analyzed>'
)
def analysis_pipeline(family):
    """Make an analysis pipeline for the exomes."""
    family_dir = os.path.join(BASE_PATH, 'exomes', family)
    
    for dirname, dirnames, filenames in os.walk(family_dir):
        # print path to all subdirectories first.
        # for subdirname in dirnames:
        #     print(os.path.join(dirname, subdirname))

        # print path to all filenames.
        for filename in filenames:  
            if filename.endswith('_qc_sampleInfo.yaml'):
                print(filename, type(str(filename)))
                print(os.path.join(dirname, filename))
                yaml_object = yaml.load(open(os.path.join(dirname, filename), mode='r', encoding='utf-8'))
                pp(yaml_object)
                pp(yaml_object[int(family)].keys())
                pp(yaml_object[int(family)]['MostCompleteVCF'])
                for individual in yaml_object[int(family)].keys():
                    print(individual)
                
                # print(yaml.dump(yaml.load(open(os.path.join(dirname, filename), mode='r', encoding='utf-8'))))
                
    
    
if __name__ == '__main__':
    analysis_pipeline()