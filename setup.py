#!/usr/bin/env python

import os
import re
from setuptools import setup

init_py = open(os.path.join('bookmarksync', '__init__.py')).read()
info = dict(re.findall("__([a-z_]+)__\s*=\s*'([^']+)'", init_py))

setup(
    name="bookmarksync",
    version=info['version'],
    packages=['bookmarksync'],
    install_requires=['lxml', 'xmldiff'],

    test_suite='tests',
    zip_safe=False,

    # metadata to display on PyPI
    author=info['author'],
    author_email=info['author_email'],
    description="Bookmark sync utility",
    license=info['license'],
    keywords="bookmark bookmarks html xml sync diff",
    url="https://github.com/jontwo/bookmark-sync",

    entry_points={
        'console_scripts': [
            'bookmarksync = bookmarksync.__main__:main'
        ]
    },
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities',
    ]
)
