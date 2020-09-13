#!/usr/bin/python3
from setuptools import find_packages
from distutils.core import setup

version = "1.0.3"

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="ofxstatement-lithuanian",
    version=version,
    author="Andrey Lebedev",
    author_email="andrey@lebedev.lt",
    url="https://github.com/kedder/ofxstatement-lithuanian",
    description=("Statement parsers for banks, operatiing in Lithuania"),
    long_description=long_description,
    license="GPLv3",
    keywords=["ofxstatement", "lithuanian"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Utilities",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["ofxstatement", "ofxstatement.plugins"],
    entry_points={
        "ofxstatement": [
            "litas-esis = ofxstatement.plugins.litas_esis:LitasEsisPlugin",
            "swedbank = ofxstatement.plugins.swedbank:SwedbankPlugin",
            "danske = ofxstatement.plugins.danske:DanskePlugin",
        ]
    },
    install_requires=["ofxstatement>=0.7.0"],
    test_suite="ofxstatement.plugins.tests",
    include_package_data=True,
    zip_safe=True,
)
