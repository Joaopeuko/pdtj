import pathlib
import setuptools

import __version__

long_description = (pathlib.Path(__file__).parent / "README.md").read_text()

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.readlines()

setuptools.setup(
    name='pdtj',
    version=__version__.version,
    license='MIT',
    author="Joao Paulo Euko",
    url='https://github.com/Joaopeuko/pdtj',
    keywords=["python", "docstring", "json"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=[requirement for requirement in requirements],
)