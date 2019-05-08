from setuptools import setup

setup(
    name='RungeKutta',
    version='1.0',
    packages=['FirstOrderODE, SecondOrderODE'],
    url='https://github.com/CarlosLopezNubes5/RungeKutta',
    license='MIT',
    author='Jose Carlos Lopez Arriaga; Ana Isabel Gutierrez Chavez',
    author_email='',
    description='Implementation of the Runge Kutta 4th order method for ODEs',
    install_requires=['numpy', 'matplotlib']
)
