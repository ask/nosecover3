#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES
import sys

packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
src_dir = "nosecover3"


def osx_install_data(install_data):

    def finalize_options(self):
        self.set_undefined_options("install", ("install_lib", "install_dir"))
        install_data.finalize_options(self)


def fullsplit(path, result=None):
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

for dirpath, dirnames, filenames in os.walk(src_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith("."):
            del dirnames[i]
    for filename in filenames:
        if filename.endswith(".py"):
            packages.append('.'.join(fullsplit(dirpath)))
        else:
            data_files.append([dirpath, [os.path.join(dirpath, f) for f in
                filenames]])

if os.path.exists("README.rst"):
    long_description = codecs.open('README.rst', "r", "utf-8").read()
else:
    long_description = "See http://pypi.python.org/pypi/nosecover3"

setup(
    name='nose-cover3',
    version="0.0.3",
    description="Coverage 3.x support for Nose",
    author="Ask Solem",
    author_email="askh@opera.com",
    url="http://github.com/ask/nosecover3",
    platforms=["any"],
    packages=packages,
    license="GNU LGPL",
    data_files=data_files,
    zip_safe=False,
    test_suite="nose.collector",
    install_requires=[
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU Library or Lesser "
            "General Public License (LGPL)",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=long_description,
    entry_points = {
        'nose.plugins': [ 'cover3 = nosecover3:Coverage3' ]
    },
)
