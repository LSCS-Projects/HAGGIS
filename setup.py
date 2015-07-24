#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='HAGGIS',
    version='0.1.0',
    description='Historical Address Geocoder',
    long_description=readme + '\n\n' + history,
    author='Konstantinos Daras',
    author_email='konstantinos.daras@gmail.com',
    url='https://github.com/gisdarcon/haggis',
    packages=[
        'haggis',
    ],
    package_dir={'haggis':
                 'haggis'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='haggis',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)