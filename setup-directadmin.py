from setuptools import setup, find_packages

setup(
    name='letsencrypt-directadmin',
    install_requires=[
        'letsencrypt',
        'zope.interface',
    ],
    packages=['letsencrypt_directadmin', 'directadmin'],
    package_dir={'letsencrypt_directadmin': 'letsencrypt_directadmin', 'directadmin': 'python-directadmin/directadmin'},
    entry_points={
        'letsencrypt.plugins': [
            'directadmin = letsencrypt_directadmin.configurator:Configurator',
        ],
    },
)