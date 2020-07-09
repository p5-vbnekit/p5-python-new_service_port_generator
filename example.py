#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import socket

from p5.new_service_port_generator import make as _make_generator


def _main():
    _generator = _make_generator()
    _pool_copy = set(_generator.pool.copy())

    for _port in _pool_copy:
        try: _name = socket.getservbyport(_port)
        except OSError: continue
        if not _name: continue
        raise RuntimeError("unexpected port found in pool (reserved in known services): #{} - {}".format(_port, _name))

    for _item in _generator:
        if not (_item in _pool_copy): raise RuntimeError("unexpected port received from generator (not in pool)")
        print("PORT: {}, LEFT: {}".format(_item, len(_generator.pool)), file = sys.stderr)


if "__main__" == __name__: _main()
