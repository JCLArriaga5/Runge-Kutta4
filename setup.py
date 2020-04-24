
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='Runge-Kutta4',
    version='1.0',
    packages=['RungeKutta'],
    url='https://github.com/JCLArriaga5/Runge-Kutta4',
    license='MIT',
    author='José Carlos López Arriaga; Ana Isabel Gutiérrez Chávez',
    author_email='josecarloslopezarriaga@gmail.com',
    description='Implementation of the Runge Kutta 4th order method for ODEs',
    install_requires=required
)
