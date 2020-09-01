#!/usr/bin/env python
"""Setup file for interator module."""

import setuptools

setuptools.setup(
    name='interator',
    version='0.1',
    author="Will Leskowitz",
    author_email="willleskowitz@gmail.com",
    packages=setuptools.find_packages(),
    url='https://github.com/willleskowitz/interator',
    description='Integer sequence generation and related conditional tests.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords=['integer', 'sequence', 'generator', 'Fibonacci', 'Lucas',
              'generalizations', 'prime', 'numbers', 'tests'],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    setup_requires=['wheel'],
    install_requires=['numpy']
)
