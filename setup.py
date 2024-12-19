from setuptools import setup, find_packages

setup(
    name='JakaModbusCommunication',                     # Your package name
    version='4.0.8',
    author='Lucas Pijl',
    author_email='lapijl@uwaterloo.ca',
    description="A Modbus helper library for Jaka communication.",
    long_description=open("README.md").read(),  # Include README content
    long_description_content_type="text/markdown",
    url="https://github.com/cacher300/JakaModbusCom",  # Replace with your repo URL
    packages=find_packages(),  # Automatically include all packages
    install_requires=[
        "pymodbus>=3.8.0",  # Required dependency
    ],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",  # Specify minimum Python version
)

