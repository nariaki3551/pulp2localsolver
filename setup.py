from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pulp2localsolver",
    packages=find_packages(),
    include_package_data=True,
    version="0.1.0",
    license="MIT",
    install_requires=[
        "pulp",
        "localsolver",
    ],
    author="nariaki tateiwa",
    author_email="nariaki3551@gmail.com",
    description="A PuLP to LocalSolver converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="optimization LP MIP modeling LocalSolver PuLP",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)

