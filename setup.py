from setuptools import setup


def getfile(filename):
    with open(filename) as file:
        return file.read()


setup(
    name='makepass',
    version='0.9.8',
    packages=[
        'makepass'
    ],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'make_pass = makepass.makepass:main',
        ],
    },
    package_data={
        'makepass': ["data/10k.txt", "data/20k.txt"]
    },
    install_requires=[
        'autocommand >=2.1.0, <3.0.0',
    ],
    platforms='any',
    license='GPLv2',
    author='Nathan West',
    url='https://github.com/Lucretiel/MakePass',
    description='A simple password generator based on https://xkcd.com/936/',
    long_description=getfile('README.rst'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
)
