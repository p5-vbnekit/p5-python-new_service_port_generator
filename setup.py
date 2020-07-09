#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools


setuptools.setup(
    name = "p5.new_service_port_generator",
    url = "https://github.com/p5-vbnekit/p5-python-new_service_port_generator",
    license = "GPL-3.0",
    version = "0.0.0",
    author = "p5-vbnekit",
    author_email = "vbnekit@gmail.com",
    package_dir = {"": "src"},
    packages = setuptools.find_namespace_packages(where = "src"),
    setup_requires = ("wheel", ),
    description = ""
)
