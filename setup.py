import sys

import setuptools
from setuptools.command.test import test as TestCommand

with open("README.md", "r") as fh:
    long_description = fh.read()


class Test(TestCommand):
    def run_tests(self):
        import pytest

        errno = pytest.main(["tests/"])
        sys.exit(errno)


REQUIRED = open("requirements.txt").read()

setuptools.setup(
    name="bcex",
    version="0.0.1",
    author="simon-bc",
    author_email="simon@blockchain.com",
    description="Websocket Client and interface for Blockchain.com Exchange",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simon-bc/bcex",
    packages=setuptools.find_packages(exclude=["tests", "scripts"]),
    cmdclass={"test": Test},
    install_requires=REQUIRED,
    tests_require=["pytest"],
    keywords=[
        "cryptocurrency",
        "bitcoin",
        "btc",
        "trading",
        "market feed",
        "market data",
        "exchange",
        "blockchain",
        "eth",
        "xlm",
        "crypto",
        "market making",
        "bot",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)