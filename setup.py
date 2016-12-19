from setuptools import setup

setup(
    name='falguard',
    version='0.1',
    author='Remy Gwaramadze',
    author_email='remy@gwaramadze.com',
    license='MIT',
    py_modules=['falguard'],
    install_requires=[
        'falcon>=1.1.0,<=2.0.0',
        'bravado_core>=4.6.0,<=5.0.0',
    ],
)
