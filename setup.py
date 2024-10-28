import io
import os
import re
from setuptools import setup, find_packages

scriptFolder = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptFolder)

# Find version info from module (without importing the module):
with open("src/nfdinspector/__init__.py", "r") as fileObj:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fileObj.read(), re.MULTILINE
    ).group(1)

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fileObj:
    long_description = fileObj.read()

setup(
    name="NFDInspector",
    version=version,
    url="https://github.com/montan-code/nfdinspector",
    author="Andreas Ketelaer",
    author_email="andreas.ketelaer@bergbaumuseum.de",
    description=(
        """A Python package to inspect formal quality problems in research data."""
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3+",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    test_suite="tests",
    install_requires=["lxml"],
    keywords="",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
