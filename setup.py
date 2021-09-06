# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="roborock-exporter",
    version="0.1.0",
    description="A prometheus exporter for roborock",
    license="AGPL",
    author="hundehausen",
    packages=['python-miio', 'prometheus_client'],
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ]
)
