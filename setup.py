# -*- coding: utf-8 -*-

from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession


def get_requirements():
    """Use requirements to fill dependencies"""
    return [str(x.req) for x in parse_requirements('requirements/base.txt',
                                                   session=PipSession())]

setup(
    name='ealpha-screener',
    version='0.1',
    py_modules=['ealpha'],
    include_package_data=True,
    install_requires=get_requirements(),
    entry_points='''
        [console_scripts]
        ealpha=ealpha:cli
    ''',
)
