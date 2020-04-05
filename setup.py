#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requisites = ['requests-html>=0.10.0', 'requests>=2.19.1', 'crayons==0.2.0']

setup(
    name='uds',
    version='0.1.6',
    description='Dictionary CLI searcher: supports Urban, Cambridge',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Viet Hung Nguyen',
    author_email='hvn@familug.org',
    url='https://github.com/hvnsweeting/uds',
    license='MIT',
    classifiers=[
        'Environment :: Console',
    ],
    scripts=['uds'],
    install_requires=requisites
)
