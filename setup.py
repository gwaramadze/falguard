from setuptools import setup

setup(
    name='falguard',
    version='0.4',
    author='Remy Gwaramadze',
    author_email='remy@gwaramadze.com',
    url='https://github.com/gwaramadze/falguard',
    description='Falcon requests validation against OpenAPI (Swagger) schema',
    long_description=open('README.rst').read(),
    license='Apache 2.0',
    py_modules=['falguard'],
    install_requires=[
        'falcon>=1.1.0,<3.0.0',
        'bravado_core>=4.6.0,<6.0.0',

        # Required for Python 3.6 and 3.7
        'six>=1.12.0',
    ],
    extras_require={
        'tests': [
            'pytest',
            'pytest-cov',
            'pytest-flake8',
            'pytest-pylint',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
    ]
)
