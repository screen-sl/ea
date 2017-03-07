# -*- coding: utf-8 -*-

"""Management commands"""

import logging
import click
import boto3
import os
import requests
import json

from jl_fixer import process_files

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

STORAGE_PLUGIN = {
  "type": "file",
  "enabled": True,
  "connection": "s3a://ea-eu-west-1-dev-tech-test/",
  "config": None,
  "workspaces": {
    "read": {
      "location": "/data",
      "writable": False,
      "defaultInputFormat": None
    },
    "write": {
      "location": "/data-export",
      "writable": True,
      "defaultInputFormat": None
    }
  },
  "formats": {
    "jsonlines": {
      "type": "json",
      "extensions": [
        "jl"
      ]
    },
    "json": {
      "type": "json",
      "extensions": [
        "json"
      ]
    }
  }
}

@click.group()
def cli():
    """Eagle Alpha Screener
    Provides the management commands to execute functionality
    of the screener.
    """


@cli.command('create-s3-bucket')
@click.option('--bucket',
              default='ea-eu-west-1-dev-tech-test',
              help='Create a bucket in S3. Function is idempotent.')
def create_s3_bucket(bucket):
    "Create S3 Bucket"
    logger.info('Creating bucket %s', bucket)
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket=bucket)
    logger.info('Bucket created.')


@cli.command('create-s3-storage-plugin')
@click.option('--name',
              default='s3',
              help='Name of the target storage plugin')
def create_s3_storage_plugin(name):
    "Configure S3 Storage Plugin"
    requests.post('http://drill:8047/storage/{0}.json'.format(name),
                  json={"name": name, "config": STORAGE_PLUGIN})

@cli.command('load-file-to-s3')
@click.option('--bucket',
              default='ea-eu-west-1-dev-tech-test',
              help='S3 Target Bucket')
@click.option('--prefix',
              default='data/',
              help='S3 Target Prefix')
@click.option('--folder',
              default='data-fixed/',
              help='Source Folder to Upload from')
def load_file_to_s3(folder, prefix, bucket):
    s3 = boto3.client('s3')
    for root, _, files in os.walk(folder):
        for file in files:
            if not '.jl' in file:
                continue
            source = os.path.join(root, file)
            target = os.path.join(*(source.split(os.path.sep)[1:]))
            target = os.path.join(prefix, target)
            logger.info('Uploading from %s', source)
            logger.info('Uploading to %s at %s', bucket, target)
            s3.upload_file(source, bucket, target)

def _query_drill(query):
    logger.info(query)
    response = requests.post('http://drill:8047/query.json',
                             json={'queryType': 'SQL',
                                   'query' : query})
    logger.info(response.status_code)

@cli.command('query-drill')
@click.option('--query',
              help='Query to run against drill',
              default='SELECT * FROM `s3`.`read`.`20170131/20170131-bestbuy.jl`')
def query_drill(query):
    """Run query against Drill"""
    _query_drill(query)


@cli.command('setup-drill')
def setup_drill():
    """Configure Drill Options"""
    _query_drill("ALTER SYSTEM SET `store.format`='jsonlines'")
    _query_drill("ALTER SYSTEM SET `store.json.read_numbers_as_double` = true")
    _query_drill("ALTER SYSTEM SET `store.json.all_text_mode` = false")


@cli.command('fix-malformed-jl')
@click.option('--inputdir',
              help='Directory of malformed files',
              default='data')
@click.option('--outputdir',
              help='Directory to output fixed files',
              default='data-fixed')
def fix_malformed_jl(inputdir, outputdir):
    process_files(inputdir, outputdir)
"""
Cols:
CAST(sku  as VARCHAR(30)), 
CAST(reg_price as VARCHAR(30)), 
CAST(crawl_date as VARCHAR(30)),  
CAST(blank_price as VARCHAR(30)), 
CAST(category as VARCHAR(30)), 
CAST(title as VARCHAR(30)), 
CAST(page_position as VARCHAR(30)), 
CAST(brand as VARCHAR(30)), 
CAST(clock as VARCHAR(30)),
CAST(publisher as VARCHAR(30)), 
CAST(colour as VARCHAR(30)), 
CAST(sort_by as VARCHAR(30)), 
CAST(price as VARCHAR(30)), 
CAST(platform as VARCHAR(30)), 
CAST(product_link_listing as VARCHAR(30)), 
CAST(product_link as VARCHAR(30)), 
CAST(model as VARCHAR(30)), 
CAST(quarter as VARCHAR(30)), 
CAST(product_name as VARCHAR(30))
"""
