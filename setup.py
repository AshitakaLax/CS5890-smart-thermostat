#!/usr/bin/env python3

from setuptools import setup, find_packages

exec(open('models/__init__.py').read())

setup(
    name='CS5890-smart-thermostat',
    version=__version__,
    description='A Smart thermostat model of energy.',
    maintainer='Ashitakalax',
    maintainer_email='leviballing@gmail.com',
    url='https://github.com/AshitakaLax/CS5890-smart-thermostat',
    packages=find_packages(exclude=['test*']),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering'
    ]
)
