from setuptools import setup, find_packages

NAME = "docker_man"
VERSION = "1.2.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools


setup(
    name=NAME,
    version=VERSION,
    description="Docker_man is the tool for managing docker containers",
    author="Artur Antonov",
    author_email="artur.antonov@perfectart.com",
    url="https://github.com/ArturAntonov/docker_man",
    license='MIT',
    keywords=["Docker", "Docker-man tools"],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'docker_man=docker_man.zapuskator:main',
        ],
    },
    long_description="""\
    This is the docker_man tool for managing docker containers (run, stop, rebuild, restart, etc]
    """
)
