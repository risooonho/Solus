"""Docstring for setup for setuptools."""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Andre Wolff',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'andre.r.wolff@gmail.com',
    'version': '1.0',
    'install_requires': ['nose', 'pygame'],
    'packages': ['solus'],
    'scripts': [],
    'name': 'Solus'}

setup(**config)
