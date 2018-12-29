from setuptools import setup

setup(
    name='falguard',
    version='0.1',
    author='Remy Gwaramadze',
    author_email='remy@gwaramadze.com',
    url='https://github.com/gwaramadze/falguard',
    description='Falcon requests validation against OpenAPI (Swagger) schema',
    long_description=open('README.rst').read(),
    license='Apache 2.0',
    py_modules=['falguard'],
    install_requires=[
        'falcon>=1.1.0,<=2.0.0',
        'bravado_core>=4.6.0,<=6.0.0',
    ],
    extras_require={
        'tests': [
            'pytest',
            'pytest-cov',
            'pytest-flakes',
            'pytest-pep8',
            'webtest',
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
        'Topic :: Software Development :: Libraries',
    ]
)
