#!/usr/bin/env python3

import argparse

from acdcli_more import shared

def main():
    args = shared.init()

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--no-filenames', action='store_true',
                        help='do not print filenames next to MD5 digests')
    parser.add_argument('nodes', nargs='+', metavar='NODE')
    args = parser.parse_args(namespace=args)

    for node_id in args.nodes:
        args.node = node_id
        shared.resolve_remote_path_args(args, ['node'])
        node = shared.cache.get_node(args.node)
        if node.md5:
            if args.no_filenames:
                print(node.md5)
            else:
                print('%s  %s' % (node.md5, node.name))
        else:
            shared.logger.error('%s has no associated MD5 digest.' % node_id)

if __name__ == "__main__":
    main()
