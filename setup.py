#!/usr/bin/env python
from setuptools import setup

from version import get_and_increment

setup(name='Documentary',
      version='1.0.0-{}'.format(get_and_increment()),
      description='Tool for creating concise, complex phpDoc',
      license='MIT',
      packages=['documentary'],
      install_requires=[
          'schema>=0.7.1',
      ],
      entry_points={
          'console_scripts': [
              'documentary = documentary.__main__:main'
          ]
      })
