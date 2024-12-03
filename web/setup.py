from setuptools import setup, find_packages

setup(
    name='cpu',
    version='0.1.0',
    description='A CPU simulator',
    author='Lukas',
    author_email='info@loreley.one',
    packages=find_packages(where='../src'),  # Look for packages in 'src'
    package_dir={'': '../src'},              # Root for packages is 'src'
    include_package_data=False,  # Include package data as specified in MANIFEST.in
    package_data={
        'cpu': ['*.asm'],
    },
)