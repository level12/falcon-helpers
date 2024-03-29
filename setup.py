import os.path
from setuptools import setup, find_packages

cdir = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(cdir, 'README.rst')).read()
CHANGELOG = open(os.path.join(cdir, 'CHANGELOG.rst')).read()

setup(
    name="falcon-helpers",
    description=('A few helpful tools to make working with the falcon '
                 'framework a real joy!'),
    long_description='\n\n'.join((README, CHANGELOG)),
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'cryptography',
        'falcon==3.*',
        'falcon_multipart',
        'jinja2',
        'marshmallow>2',
        'marshmallow-sqlalchemy',
        'pyjwt>=2.4',
        'sqlalchemy<2',
        'requests',
        'ujson',
        'wrapt',
    ],

    extras_require={
        's3': ['boto3'],
        'cli': ['click'],
        'dev': [
            'moto',
            'click',
            'pytest>4',
            'raven',
        ]
    },
    zip_safe=True,
    license='BSD',
    author="Nick Zaccardi",
    author_email="nicholas.zaccardi@gmail.com",
    url='https://github.com/level12/falcon-helpers',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
