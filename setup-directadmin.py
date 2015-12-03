from setuptools import setup

setup(
    name='letsencrypt-directadmin',
    install_requires=[
        'letsencrypt',
        'zope.interface',
        'python-directadmin>=0.6.1'
    ],
    packages=['letsencrypt_directadmin'],
    dependency_links = ['http://github.com/sjerdo/python-directadmin/tarball/master#egg=python-directadmin-0.6.1'],
    package_dir={'letsencrypt_directadmin': 'letsencrypt_directadmin'},
    entry_points={
        'letsencrypt.plugins': [
            'directadmin = letsencrypt_directadmin.configurator:Configurator',
        ],
    },
)