#!/usr/bin/env python3

"""
Initialize cache, logger, etc. and parse global options.

See other existing scripts for usage.
"""

import argparse
import os
import sys

import acd_cli
import acdcli
from acd_cli import (
    acd_client, cache, logger,
    resolve_remote_path_args
)
from acdcli.cache import format, db

def _parse_global_args(argv, namespace=None):
    opt_parser = argparse.ArgumentParser()

    # The following global args handling code was directly copied from
    # acd_cli.py -- https://git.io/vgS1Z -- except that I switched the
    # default of --check from full to none (it makes no sense to check
    # the integrity of a ~1GB databse with every single operation).
    log_group = opt_parser.add_mutually_exclusive_group()
    log_group.add_argument('-v', '--verbose', action='count',
                           help='prints some info messages to stderr; '
                                'use "-vv" to also get sqlalchemy info')
    log_group.add_argument('-d', '--debug', action='count',
                           help='prints info and debug to stderr; '
                                'use "-dd" to also get sqlalchemy debug messages')
    opt_parser.add_argument('-nl', '--no-log', action='store_false', dest='log',
                            help='do not save a log of debug messages')
    opt_parser.add_argument('-c', '--color', default=format.ColorMode['never'],
                            choices=format.ColorMode.keys(),
                            help='"never" [default] turns coloring off, '
                                 '"always" turns coloring on '
                                 'and "auto" colors listings when stdout is a tty '
                                 '[uses the Linux-style LS_COLORS environment variable]')
    opt_parser.add_argument('-i', '--check', default=db.NodeCache.IntegrityCheckType['none'],
                            choices=db.NodeCache.IntegrityCheckType.keys(),
                            help='select database integrity check type [default: none]')
    opt_parser.add_argument('-u', '--utf', action='store_true',
                            help='force utf output')
    opt_parser.add_argument('-nw', '--no-wait', action='store_true', help=argparse.SUPPRESS)

    return opt_parser.parse_args(argv, namespace)

def init(init_cache=True, init_client=False):
    global acd_client
    global cache
    global logger

    global_opt_str = os.environ.get('ACDCLI_GLOBAL_OPTS', '')
    args = _parse_global_args(global_opt_str.split(':') if global_opt_str else [])

    acd_cli.set_log_level(args)
    logger = acd_cli.logger

    if init_cache:
        cache = acdcli.cache.db.NodeCache(acd_cli.CACHE_PATH, args.check)
        acd_cli.cache = cache

    if init_client:
        acd_client = acdcli.api.client.ACDClient(acd_cli.CACHE_PATH)
        acd_cli.acd_client = acd_client

    return args
