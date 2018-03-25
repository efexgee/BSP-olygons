from setuptools import setup, find_packages

setup(
    name='polytree',
    version='0.5',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'pytest',
        'Pillow',
    ],
    author='Falko Goettsch',
    #author_email='',
)
