from setuptools import setup
from setuptools import find_packages

long_description = """
# spider
A package for python.
Markdown description
"""

setup(
    name="spider",
    version="0.0.1",
    author="Jacob Hart",
    url="https://github.com/jdchart/spider-python",
    license="GLPv3+",
    author_email="jacob.dchart@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Use spider in python.",
    packages=find_packages()
)