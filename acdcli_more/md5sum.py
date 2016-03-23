#!/usr/bin/env python3

import argparse

from acdcli_more import shared

def print_md5s(node, recursive=True, no_filenames=False):

    def print_md5(node):
        if node.md5:
            if no_filenames:
                print(node.md5)
            else:
                print('%s  %s' % (node.md5, node.name))
        else:
            raise LookupError

    if node.type == 'file':
        print_md5(node)
    elif recursive:
        folders, files = shared.cache.list_children(node.id)
        for d in folders:
            print_md5s(d, recursive, no_filenames)
        for f in files:
            print_md5(f)
    else:
        raise IsADirectoryError

def main():
    args = shared.init()

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--no-filenames', action='store_true',
                        help='do not print filenames next to MD5 digests')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='recurse into directories and subdirectories')
    parser.add_argument('nodes', nargs='+', metavar='NODE')
    args = parser.parse_args(namespace=args)

    for node_id in args.nodes:
        args.node = node_id
        shared.resolve_remote_path_args(args, ['node'])
        node = shared.cache.get_node(args.node)
        try:
            print_md5s(node, recursive=args.recursive, no_filenames=args.no_filenames)
        except IsADirectoryError:
            shared.logger.error('%s is a directory.' % node_id)
        except LookupError:
            shared.logger.error('%s has no associated MD5 digest.' % node_id)

if __name__ == "__main__":
    main()
