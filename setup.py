from setuptools import setup, find_packages

setup(
    name='JakaModbusCommunication',                     # Your package name
    version='4.0.4',
    author='Lucas Pijl',
    author_email='lapijl@uwaterloo.ca',
    description="A Modbus helper library for Jaka communication.",
    long_description=open("README.md").read(),  # Include README content
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jaka_modbus_coms",  # Replace with your repo URL
    packages=find_packages(),  # Automatically include all packages
    install_requires=[
        "pymodbus>=2.5.0",  # Required dependency
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Specify minimum Python version
)

