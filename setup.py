# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'myproject',
    version      = '1.0',
    packages     = find_packages(),
    package_data = {'myproject': ['resources/*.json']},
    entry_points = {'scrapy': ['settings = data_grab.settings']},
    zip_safe=False,
)
