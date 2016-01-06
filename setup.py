import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
  name='zdns',
  version='0.0.1',
  description='Python utility for quickling doing DNS resolution on a large
  number of domains',
  license="Apache License, Version 2.0",
  long_description=open(os.path.join(here, 'README.md')).read(),
  classifiers=[
    "Programming Language :: Python",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English"
  ],
  author='ZMap Team',
  author_email='zmap-team@umich.edu',
  url='https://github.com/zmap/zdns',
  keywords='zmap censys zdns internet-wide scanning',
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  install_requires = [
    "dnspython",
  ],
  entry_points = {
    'console_scripts': [
      'zdns = zdns.__main__:main',
    ]
  }
)
