from setuptools import setup, find_packages

NAME = "docker_man"
VERSION = "1.0.1"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools


setup(
    name=NAME,
    version=VERSION,
    description="Docker-man tool for managing containers",
    author="Artur Paulson",
    author_email="artur.antonov@perfectart.com",
    url="https://github.com/ArturAntonov/docker-man",
    license='MIT',
    keywords=["Docker", "Docker-man tools"],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'docker_man=docker_man.zapuskator:main',
        ],
    },
    long_description="""\
    This is a docker-man tool for managing docker containers (run, stop, rebuild, etc]
    """
)
