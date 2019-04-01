from setuptools import setup

setup(
    name='sca3300',
    description='SCA3300 Linux driver with dependency on just `spidev`',
    long_description='SCA3300 3-axis Murata accelerometer driver for Linux platforms.',
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