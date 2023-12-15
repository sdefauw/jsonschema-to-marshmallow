import io
import os

from setuptools import setup, find_namespace_packages


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def read(fname):
    with io.open(fname) as fp:
        return fp.read()


long_description = read("README.md")


setup(
    name="jsonschema-to-marshmallow",
    version="0.1.0",
    description="Get Marshmallow class from JSON Schema",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sebastien De Fauw",
    author_email="sdefauw@gmail.com",
    url="https://github.com/sdefauw/mjsonschema-to-marshmallow",
    packages=find_namespace_packages(include=['jsonschema_marshmallow.*']),
    include_package_data=True,
    install_requires=[
        "jsonschema",
        "marshmallow>=3.19.0",
    ],
    license="MIT License",
    zip_safe=False,
    keywords=(
        "jsonschema"
        "marshmallow"
    ),
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    test_suite="tests",
)