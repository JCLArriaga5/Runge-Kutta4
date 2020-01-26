import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='RungeKutta',
    version='1.0',
    packages=['FirstOrderODE, SecondOrderODE'],
    url='https://github.com/CarlosLopezNubes5/RungeKutta',
    license='MIT',
    author='José Carlos López Arriaga; Ana Isabel Gutiérrez Chávez',
    author_email='',
    description='Implementation of the Runge Kutta 4th order method for ODEs',
    install_requires=required
)
