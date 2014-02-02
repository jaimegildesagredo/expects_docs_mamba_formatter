# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='expects_docs_mamba_formatter',
    version='0.1.0',
    description='Mamba formatter to build the Expects docs',
    author='Jaime Gil de Sagredo Luna',
    author_email='jaimegildesagredo@gmail.com',
    license='Apache 2.0',
    py_modules=['expects_docs_mamba_formatter'],
    entry_points={
        'mamba.formatters': [
            'expects_docs = expects_docs_mamba_formatter:RSTFormatter'
        ]
    },
    classifiers=[
    ]
)
