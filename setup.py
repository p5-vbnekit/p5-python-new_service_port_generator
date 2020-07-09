#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools


def _make_long_description():
    with open("README.md", "r") as _stream: return _stream.read()


setuptools.setup(
    name = "p5.new_service_port_generator",
    url = "https://github.com/p5-vbnekit/p5-python-new_service_port_generator",
    license = "GPL-3.0",
    version = "0.0.1",
    author = "p5-vbnekit",
    author_email = "vbnekit@gmail.com",
    long_description = _make_long_description(),
    long_description_content_type = "text/markdown",
    package_dir = {"": "src"},
    packages = setuptools.find_namespace_packages(where = "src"),
    setup_requires = ("wheel", ),
    description = ""
)
