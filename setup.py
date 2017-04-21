from setuptools import setup
import sys

dependencies = [
    'autocommand >=2.1.0, <3.0.0',
]

# TODO: I'm concerned that this won't work as well as I hope. In particular,
# I'm worried that, if a wheel or source distribution is produced, the
# dependencies are encoded directly, rather than using the setup.py logic.
if sys.version_info < (3, 4):
    dependencies.append('pathlib2')

setup(
    name='makepass',
    version='0.9.0',
    packages=[''],
    package_dir={'': 'src'},
    data_files=[
        ('share/makepass/', [
            'data/10k.txt',
            'data/20k.txt',
        ]),
    ],
    entry_points={
        'console_scripts': [
            'make_pass = makepass:main',
        ],
    },
    install_requires=dependencies,
    platforms='any',
    license='GPLv2',
    author='Nathan West',
    url='https://github.com/Lucretiel/MakePass',
    description='A simple password generator based on https://xkcd.com/936/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
)