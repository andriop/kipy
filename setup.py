#!/usr/bin/env python

from setuptools import setup, find_packages

packages = ['kipy.' + p for p in find_packages('kipy', exclude=['test', 'test*', '*.t'])]
packages.append('kipy')
    
setup(
    name='kipy',
    version='1.0.1',
    author='Patrick Maupin',
    author_email=' pmaupin@gmail.com',
    url='pyeda.org',
    license='OSI-approved MIT license',
    description='Provides useful scripts around KiCad.',
    packages=packages
)
