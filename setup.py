from setuptools import setup

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2",
    "Topic :: Software Development :: Libraries",
]

setup(
    name='Flask-bitjws',
    version='0.1.0.1',
    packages=['flask_bitjws'],
    include_package_data=True,
    url='https://github.com/deginner/flask-bitjws',
    license='MIT',
    classifiers=classifiers,
    author='deginner',
    author_email='support@deginner.com',
    description='A Flask extension for bitjws authentication.',
    setup_requires=['pytest-runner'],
    install_requires=[
        "Flask",
        'secp256k1==0.11',
        "bitjws==0.6.3.1",
    ],
    tests_require=['pytest', 'pytest-cov']
)

