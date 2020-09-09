#!usr/bin/env python

from setuptools import setup, find_packages

setup(name="gdrive_io",
	version="0.1.2",
    author="",
    author_email="",
	description="Easy to input files on GoogleDrive as pandas DataFrame fortmat and output(upload) DataFrames onto GoogleDrive powered by Pandas and Pydrive.",
	url="https://github.com/mi-ta-d/gdrive_io",
	packages=find_packages(),
	python_requires='>=3.6',
	)
