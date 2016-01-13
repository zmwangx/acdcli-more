=============
 acdcli-more
=============

More commands for `acdcli`.

Usage
=====

Commands (console scripts) provided by this package are best used alongside my
`acdcli Prezto module
<https://github.com/zmwangx/prezto/tree/master/modules/acdcli>`_, which
converts external commands of the form ``acdcli-command`` into subcommands of
``acdcli``, and provides completion.

Commands
========

* ``acdcli-trees``: Like `tree`, but print sizes of each node, including
  directory nodes. The size of a directory node is the sum of its children's
  sizes.

For detailed option breakdown of each command, run ``--help`` with the
respective command.

License
=======

Copyright (C) 2016 Zhiming Wang

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see http://www.gnu.org/licenses/.

Disclaimer
----------

I'm not a fan of GPL, but it is forced upon me by `acdcli`.
