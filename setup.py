from setuptools import setup, find_packages

setup(
    name='macbook-cleaner',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'macbook-cleaner = cleaner.app:main',
        ],
    },
    python_requires='>=3.8',
)
