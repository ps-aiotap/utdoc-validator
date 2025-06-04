from setuptools import setup, find_packages

setup(
    name='utdoc_validator',
    version='0.1',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'utdoc-validator=utdoc_validator.cli:main'
        ]
    },
)