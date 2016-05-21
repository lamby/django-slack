#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-slack',

    url="https://chris-lamb.co.uk/projects/django-slack",
    version='5.7.0',
    description="Provides easy-to-use integration between Django projects and "
        "the Slack group chat and IM tool.",

    author="Chris Lamb",
    author_email="chris@chris-lamb.co.uk",
    license="BSD",

    packages=find_packages(),
    include_package_data=True,
    install_requires=(
        'Django>=1.8.0',
        'requests',
        'six',
    ),
)
