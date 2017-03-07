# -*- coding: utf-8 -*-

"""Fix malformed jsonlines file"""

import re
import os

def _fix_record(record):
    """Fix input record with missing quote"""
    try:
        result = re.sub(r"\"reg_price\":\s+?(\d+(\.\d+)?)?\s*?\"\s*?,", r'"reg_price":"\1",', record)
    # TODO: Import correct exception
    except Exception as e:
        result = re.sub(r"\"reg_price\":\s+?(\d+(\.\d+)?)?\s*?\"\s*?,", r'"reg_price":"0",', record)
    try:
        result = re.sub(r"\"price\":\s+?(\d+(\.\d+)?)?\s*?\"\s*?,", r'"price":"\1",', result)
    # TODO: Import correct exception
    except Exception as e:
        result = re.sub(r"\"price\":\s+?(\d+(\.\d+)?)?\s*?\"\s*?,", r'"price":"0",', result)
    return result

def process_files(inputdir, outputdir):
    """Stream in file and replace"""
    for root, _, files in os.walk(inputdir):
        for file in files:
            if '.jl' not in file:
                continue
            in_file = os.path.join(root, file)
            out_file = os.path.join(outputdir, *(in_file.split(os.path.sep)[1:]))
            if not os.path.exists(os.path.dirname(out_file)):
                os.mkdir(os.path.dirname(out_file))
            output = open(out_file, 'w')
            with open(in_file, 'r') as jl_file:
                for line in jl_file:
                    output.write(_fix_record(line))
            output.close()
