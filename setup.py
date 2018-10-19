import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="pymagisto",
    version="0.1",
    url="https://github.com/alejandrojnm/pymagisto",
    license='GPLv3',
    author="Alejandro JNM",
    author_email="alejandrojnm@gmail.com",
    description="Wrapper for magisto api",
    long_description=read("pymagisto/README.rst"),
    packages=find_packages(exclude=('tests',)),
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
