# -*- coding: utf-8 -*-
"""
==============
ConsoleDialogs
==============

A pure console replacement for the Robot Framework Dialogs library.
"""

from setuptools import setup, find_packages

version = '0.1.0'

install_requires = ['setuptools', 'wheel', 'robotframework']
dev_require = []

setup(name='robotframework-consoledialogs',
      version=version,
      description="A pure console replacement for the Robot Framework Dialogs library.",
      classifiers=[
          "Framework :: Robot Framework",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Environment :: Console :: Curses",
          "Operating System :: OS Independent"
      ],
      keywords='robotframework dialogs ui',
      author='tw39124-1',
      url='http://pypi.org/pypi/robotframework-consoledialogs',
      license='MIT',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={
          'dev': dev_require
      })
