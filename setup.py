# setup.py
from setuptools import setup, find_packages

setup(
    name='letsid',
    version='0.1.0',
    author='Subspace Network',
    author_email='info@subspace.network',
    description='LetsID.ai is a free service provided by Autonomys Labs that allows users to easily create, register, and manage an Auto ID.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/subspace/letsid',
    packages=find_packages(),
    install_requires=[
        'auto-sdk>=0.1.6',
        'Flask>=1.1.2',
        'Flask-Cors>=3.0.10',
        'Flask-Dance>=3.0.0',
        'PyJWT>=2.0.0',
        'python-dotenv>=0.15.0',
        'requests>=2.25.1',
    ],
    entry_points={
        'console_scripts': [
            'letsid=src.cli.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
