# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

__docformat__ = "reStructuredText"


from setuptools import setup, find_packages

setup(
    name='crate-viz',
    version='0.0.0',
    url='https://github.com/chaudum/crate-viz',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    namespace_packages=['crate'],
    entry_points={
      'console_scripts': [
        'app=crate.viz.server:main',
        'crawl=crate.viz.crawler:main',
      ],
    },
    extras_require=dict(
    ),
    install_requires = [
        'setuptools',
        'tornado',
        'crate[sqlalchemy]',
        ]
)
