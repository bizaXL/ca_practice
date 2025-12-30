from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ca_practice/__init__.py
from ca_practice import __version__ as version

setup(
    name="ca_practice",
    version=version,
    description="CA Practice Management",
    author="Your Name",
    author_email="your@email.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
