#!/usr/bin/env python

from distutils.core import setup

import os
import os.path

def recurse(path):
    B = 'hcomments'
    output = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(B, path)):
        for d in filter(lambda x: x[0] == '.', dirnames):
            dirnames.remove(d)
        for f in filenames:
            output.append(os.path.join(dirpath, f)[len(B)+1:])
    return output

setup(name='hcomments',
    version='0.1',
    description='django hierarchical comments',
    author='dvd',
    author_email='dvd@develer.com',
    packages=[
        'hcomments',
        'hcomments.management',
        'hcomments.migrations',
        'hcomments.templatetags',
    ],
    package_data={
        'hcomments': sum(map(recurse, ('locale', 'static', 'templates')), []),
    },
    install_requires=[
        'django-mptt',
    ],
)
