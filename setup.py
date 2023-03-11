from setuptools import setup, find_packages
from wolai import __version__, __author__


with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]


def long_description():
    with open('README.md', 'r') as readme:
        return readme.read()


setup(
    name='wolai-python',
    version=__version__,
    packages=find_packages(),

    author=__author__,
    author_email='ricterzheng@gmail.com',
    keywords=['wolai', 'Python', 'SDK'],
    description='wolai unofficial Python SDK',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/RicterZ/wolai-python',
    download_url='https://github.com/RicterZ/wolai-python/tarball/master',
    include_package_data=True,
    zip_safe=False,

    install_requires=requirements,
    license='MIT',
)
