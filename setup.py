 #!/usr/bin/env python
"""Setup file for interator module."""

import setuptools

setuptools.setup(
    name='interator_willleskowitz',
    version='0.1',
    author="Will Leskowitz",
    author_email="willleskowitz@gmail.com",
    packages=setuptools.find_packages(),
    url='https://github.com/willleskowitz/interator/',
    description='Integer sequence generation and related functions for conditional statements.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords='integer sequence generator conditional tests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)