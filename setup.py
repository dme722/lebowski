from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='lebowski',
  version='1.1.1',
  description='Lebowski lazy importer',
  author='Drew Ellison',
  author_email='dme722@gmail.com',
  packages = find_packages(),
  include_package_data = True,
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/dme722/lebowski',
  keywords='lazy import',
  project_urls={  # Optional
        'Bug Reports': 'https://github.com/dme722/lebowski/issues',
        'Source': 'https://github.com/dme722/lebowski',
    },
 )