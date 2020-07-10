#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import random


def _validate_port(value):
    if not isinstance(value, int): raise TypeError("invalid port, [0:65535] integer expected")
    if not (0 <= value): raise ValueError("invalid port, [0:65535] integer expected")
    if not (65536 > value): raise ValueError("invalid port, [0:65535] integer expected")


def _validate_port_range(minimum, maximum):
    try:
        try: _validate_port(minimum)
        except Exception: raise ValueError("invalid minimum")
        try: _validate_port(maximum)
        except Exception: raise ValueError("invalid maximum")
        if not (minimum < maximum): raise ValueError("minimum is not less than maximum")
    except Exception: raise ValueError("invalid range")


def _make_default_excluded():
    _list = [
        (0, 1024),  # common system reserved
        (1024, 4999),  # BSD dynamic ports
        (1025, 5000),  # Windows dynamic ports (before Vista)
        (49152, 65535),  # IANA dynamic ports
        (32768, 61000)  # Linux dynamic ports: /proc/sys/net/ipv4/ip_local_port_range
    ]

    def _make_set():
        _result = set()

        for _minimum, _maximum in _list:
            for _port in range(_minimum, _maximum): _result.add(_port)

        return _result

    _set = _make_set()
    _cache = [None, None]

    def _check(port):
        if port in _set: return False
        try:
            if socket.getservbyport(port): return False
        except OSError: return True
        return False

    def _flush():
        _minimum, _maximum = _cache
        if _minimum is None: return
        _list.append(_minimum if (_maximum is None) else (_minimum, _maximum))
        _cache[0] = _cache[1] = None

    for _current in range(0, 65536):
        if _check(_current):
            _flush()
            continue
        if _cache[0] is None: _cache[0] = _current
        else: _cache[1] = _current

    _flush()

    return tuple(_list)


class Defaults(object):
    source = range(0, 65535)
    excluded = _make_default_excluded()
    selector = random.choice


def make_pool(source = None, excluded = None):
    if source is None: source = Defaults.source
    if excluded is None: excluded = Defaults.excluded

    _excluded = set()

    def _parse_excluded():
        def _parse_one(item):
            try: _minimum, _maximum = item
            except TypeError:
                _validate_port(item)
                _excluded.add(item)
                return
            _validate_port_range(minimum = _minimum, maximum = _maximum)
            for _port in range(_minimum, 1 + _maximum): _excluded.add(_port)
        for _item in excluded: _parse_one(_item)

    _parse_excluded()

    def _make_result():
        _result = []
        for _port in source:
            _validate_port(_port)
            if not (_port in _excluded): _result.append(_port)
        return _result

    return _make_result()


Defaults.source = tuple(make_pool())


class Object(object):
    @property
    def pool(self): return self.__pool

    @property
    def selector(self): return self.__selector

    def __iter__(self):
        while self.__pool: yield self.__call__()

    def __call__(self, selector = None):
        if selector is None: selector = self.__selector
        _item = selector(self.__pool)
        self.__pool.remove(_item)
        return _item

    def __init__(self, source = None, selector = None):
        super().__init__()
        self.__pool = make_pool(source = source, excluded = tuple())
        self.__selector = Defaults.selector if (selector is None) else selector


def make(*args, **kwargs): return Object(*args, **kwargs)
