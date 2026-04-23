from pathlib import Path

from setuptools import find_packages, setup


README = Path(__file__).with_name("README.md").read_text(encoding="utf-8")

setup(
    name="JakaModbusCommunication",
    version="4.0.9",
    author="Lucas Pijl",
    author_email="lapijl@uwaterloo.ca",
    description="A Modbus helper library for Jaka communication.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cacher300/JakaModbusCom",
    packages=find_packages(),
    install_requires=[
        "pymodbus>=3.8.0",
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)

