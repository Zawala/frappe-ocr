from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ocr/__init__.py
from ocr import __version__ as version

setup(
	name="ocr",
	version=version,
	description="get test from images and pdf",
	author="zw",
	author_email="kelvin@durihub.co.zw",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
