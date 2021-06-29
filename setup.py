import io
import os.path
from setuptools import setup

VERSION_PATH = os.path.join(
    os.path.dirname(__file__), 'plotmoving/VERSION.txt')
with io.open(VERSION_PATH, 'r', encoding='utf-8') as f:
    version = f.read().strip()

setup(
    name="schedulermanager",  # what you want to call the archive/egg
    version=version,
    packages=["schedulermanager"],  # top-level python modules you can import like
    #   'import foo'
    dependency_links=[],  # custom links to a specific project
    install_requires=[],
    extras_require={},  # optional features that other packages can require
    #   like 'plotmoving[foo]'
    package_data={"schedulermanager": ["VERSION.txt"]},
    author="Tue Dang",
    author_email="dangtritue@gmail.com",
    description="The familiar example program in Python",
    license="Apache 2.0",
    keywords="example documentation tutorial",
    url="https://github.com/tuedang",
    entry_points={
        "console_scripts": [  # command-line executables to expose
            "helloworld_in_python = plotmoving.main:main",
        ],
        "gui_scripts": []  # GUI executables (creates pyw on Windows)
    }
)
