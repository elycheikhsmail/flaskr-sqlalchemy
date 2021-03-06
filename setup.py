import io

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='flaskr',
    version='1.0.0',
    url= "https://github.com/elycheikhsmail/flaskr-sqlalchemy"
    license='BSD',
    maintainer='Ely Cheikh',
    description='The basic blog app built in the Flask tutorial with sqlachemy',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-sqlalchemy'
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
