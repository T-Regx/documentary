#!/usr/bin/env python
from setuptools import setup, find_packages

from version import get_and_increment

setup(name='Documentary',
      python_requires='~=3.6',
      version='1.0.0.post{}'.format(get_and_increment()),
      description='Tool for creating concise, complex phpDoc',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'schema>=0.7.1',
      ],
      entry_points={
          'console_scripts': [
              'documentary = documentary.__main__:main'
          ]
      })
