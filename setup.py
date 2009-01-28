from setuptools import setup, find_packages

setup(
    name='Smooshy',
    description='Automatic lossless image compression',
    author='Oliver Beattie',
    author_email='oliver@obeattie.com',
    url='http://github.com/obeattie/smooshy-py/',
    version='0.1',
    install_requires=['simplejson', ],
    packages=['smooshy', ],
    entry_points={
        'console_scripts': [
            'smooshy = smooshy.smoosher:main',
        ]
    }
)
