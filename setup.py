"""
Land Surface Data Toolkit
A Python toolkit for land surface data acquisition and processing.
"""

from setuptools import setup, find_packages
import os

# Read long description from README
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='landsurface-toolkit',
    version='0.1.0',
    author='Land Surface Research Team',
    author_email='',
    description='Python toolkit for land surface data acquisition and processing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/landsurface-toolkit',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Hydrology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.9',
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.0',
            'pytest-cov>=4.0',
            'black>=23.0',
            'flake8>=6.0',
            'mypy>=1.0',
        ],
        'docs': [
            'sphinx>=5.0',
            'sphinx-rtd-theme>=1.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'lst-download=landsurface.cli:download',
            'lst-process=landsurface.cli:process',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
