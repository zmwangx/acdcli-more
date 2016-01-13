#!/usr/bin/env python3

"""This module adds a ``trees_format`` method to
```acdcli.cache.db.NodeCache`` for displaying trees with sizes, or for
calculating the total size of a tree. There is a console script
``acdcli-trees`` associated to this module.
"""

# TODO: Handle global arguments in the env var ACDCLI_GLOBAL_OPTS.

import argparse
import logging
import os
import sys

import acd_cli
from acdcli.cache import db, format
import appdirs
from zmwangx.humansize import humansize

_app_name = 'acd_cli'

logger = logging.getLogger(_app_name)

cp = os.environ.get('ACD_CLI_CACHE_PATH')
CACHE_PATH = cp if cp else appdirs.user_cache_dir(_app_name)

class NodeCache(db.NodeCache):

    def trees_format(self, node, path='.', trash=False, dir_only=False,
                     depth=0, max_depth=None, human_readable=False, numfmt=False, base10=False,
                     progress=False) -> 'Tuple[int, List[str]]':
        """Tree format with size."""

        folders, files = self.list_children(node.id, trash=trash)
        if progress:
            print("processing %s - %d subdirectories, %d files" %
                  (format.dir_fmt % path, len(folders), len(files)),
                  file=sys.stderr)

        # no_lines is for directories that is deeper than max_depth but
        # is still being processed for tree size calculation. The return
        # value for such directories will be (size, 0).
        no_lines = max_depth is not None and depth > max_depth

        lines = []
        tree_size = 0
        for folder in folders:
            folder_size, folder_lines = self.trees_format(folder, '%s/%s' % (path, folder.name),
                                                          trash, dir_only, depth + 1, max_depth,
                                                          human_readable, numfmt, base10, progress)
            tree_size += folder_size
            if not no_lines:
                lines.extend(folder_lines)

        fmt = '%s[%5s]  %s' if human_readable else '%s[%15s]  %s'
        size2print = lambda s: humansize(s, prefix='si' if base10 else 'iec', unit='',
                                         numfmt=numfmt) if human_readable else str(s)
        indent = ' ' * 4 * (depth + 1)
        for file in files:
            tree_size += file.size
            if not (dir_only or no_lines):
                lines.append(fmt % (indent, size2print(file.size),
                                    format.color_path(file.simple_name)))

        if no_lines:
            return (tree_size, [])
        else:
            this_line = fmt % (' ' * 4 * depth, size2print(tree_size),
                               format.color_path(node.simple_name))
            return (tree_size, [this_line] + lines)


def main():
    format.init(format.ColorMode['auto'])

    parser = argparse.ArgumentParser()
    parser.add_argument('--include-trash', '-t', action='store_true')
    parser.add_argument('--dir-only', '-d', action='store_true')
    parser.add_argument('--max-depth', '-L', type=int)
    parser.add_argument('--no-human-readable', action='store_true',
                        help="""show sizes in plain byte counts""")
    parser.add_argument('--numfmt', action='store_true',
                        help="""use numfmt(1) styled sizes (at most one decimal place)""")
    parser.add_argument('--si', '--base10', action='store_true',
                        help="""show sizes in SI (base 10) units; defaul is IEC (base 2)""")
    parser.add_argument('-P', '--progress', action='store_true',
                        help="""show progress information when gathering information""")
    parser.add_argument('node', nargs='?', default='/', help='root directory for the tree')
    args = parser.parse_args()

    cache = NodeCache(CACHE_PATH, check=db.NodeCache.IntegrityCheckType['none'])
    acd_cli.cache = cache

    acd_cli.resolve_remote_path_args(args, ['node'])

    node = cache.get_node(args.node)
    kwargs = {
        'trash': args.include_trash,
        'dir_only': args.dir_only,
        'max_depth': args.max_depth,
        'human_readable': not args.no_human_readable,
        'numfmt': args.numfmt,
        'base10': args.si,
        'progress': args.progress,
    }
    tree_size, lines = cache.trees_format(node, **kwargs)

    if args.progress:
        sys.stderr.write('\n')
    print('\n'.join(lines))

if __name__ == "__main__":
    main()
