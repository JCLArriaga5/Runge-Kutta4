# -*- coding: utf-8 -*-

import io
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with io.open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='Runge-Kutta4',
    version='1.0.0',
    description='Implementation of the Runge Kutta 4th order method for ODEs',
    author='José Carlos López Arriaga; Ana Isabel Gutiérrez Chávez',
    author_email='josecarloslopezarriaga@gmail.com',
    url='https://github.com/JCLArriaga5/Runge-Kutta4',
    license='MIT',
    install_requires=required,
    packages=['RungeKutta'],
    include_package_data=True,
)
