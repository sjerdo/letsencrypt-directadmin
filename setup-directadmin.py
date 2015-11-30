from setuptools import setup

setup(
    name='letsencrypt-directadmin',
    py_modules = ['directadmin'],
    install_requires=[
        'letsencrypt',
        'zope.interface',
    ],
    entry_points={
        'letsencrypt.plugins': [
            'directadmin = directadmin:Configurator',
        ],
    },
)