from setuptools import setup

setup(
    name='dtf',
    description='Documentation Testing Framework',
    version='0.1.dev',
    license='Apache',
    url='http://cyborginstitute.org/projects/dtf',
    packages=['dtf'],
    test_suite=None,
    entry_points={
        'console_scripts': [
            'dtf = dtf.dtf:main',
            'dtu = dtf.dtu:main',
            ],
        }
    )
