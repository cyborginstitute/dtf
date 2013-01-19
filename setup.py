from setuptools import setup

REQUIRES = ['pyyaml']

if version_info < (2, 7):
    # no argparse in 2.6 standard
    REQUIRES.append('argparse')

setup(
    name='dtf',
    description='Documentation Testing Framework',
    version='0.1.dev',
    license='Apache',
    url='http://cyborginstitute.org/projects/dtf',
    packages=['dtf'],
    install_requires=REQUIRES
    test_suite=None,
    entry_points={
        'console_scripts': [
            'dtf = dtf.dtf:main',
            ],
        }
    )
