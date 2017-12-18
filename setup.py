#!/usr/bin/env python3
#
# The purpose of this script is to enable uploading xdot.py to the Python
# Package Index, which can be easily done by doing:
#
#   python3 setup.py sdist upload
#
# See also:
# - https://packaging.python.org/distributing/
# - https://docs.python.org/3/distutils/packageindex.html
#

from setuptools import setup

setup(
    name='GDot',
    version='0.1',
    author='Thomas Pointhuber',
    author_email='thomas.pointhuber@gmx.at',
    url='https://github.com/pointhi/GDot',
    description="Interactive editor and viewer for Graphviz dot files",
    long_description="""
        GDot is an editor and viewer for graphs written in Graphviz's dot
        language based on xdot.
        """,
    license="GPL3+",

    install_requires=['xdot', 'graphviz'],
    packages=['gdot'],
    package_data={'': ['gdot.glade']},
    entry_points=dict(gui_scripts=['gdot=gdot.gdot:main']),

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Environment :: X11 Applications :: GTK',

        'Intended Audience :: Information Technology',

        'Operating System :: OS Independent',

        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',

        'Topic :: Multimedia :: Graphics :: Editors',
        'Topic :: Multimedia :: Graphics :: Viewers',
    ],

    # This is true, but doesn't work realiably
    #install_requires=['gi', 'gi-cairo'],
)
