"""
setup file for package description, content etc.
"""

from setuptools import setup
from os import path
from utils.version import __VERSION__

# read the contents of your README file
current_dir = path.abspath(path.dirname(__file__))
with open(path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='sca3300',
    description='SCA3300 Linux driver with dependency on just spidev',
    version=__VERSION__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>3.4.0',
    url='https://github.com/algebratech/sca3300-driver',
    author='Algebra Global, Inc',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Hardware',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='sca3300 raspberry pi acceleration spi device hardware',
    py_modules=['sca3300', 'utils']
)
