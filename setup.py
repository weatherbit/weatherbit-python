import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="pyweatherbit",
    version="2.2.1",
    author="Colin Craig",
    author_email="admin@weatherbit.io",
    description=("A python weather api wrapper for the Weatherbit.io API."),
    license="MIT",
    keywords="weather API python wrapper weatherbit.io location",
    url="http://www.weatherbit.io",
    packages=['weatherbit'],
    package_data={'weatherbit': ['LICENSE.txt', 'README.md']},
    long_description=open('README.md').read(),
    install_requires=['requests>=1.6', 'responses'],
)