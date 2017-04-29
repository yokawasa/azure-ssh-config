import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

with open('azuresshconfig.py', 'r') as fd:
    version = re.search(
        r'^_AZURE_SSH_CONFIG_VERSION\s*=\s*[\'"]([^\'"]*)[\'"]',
        fd.read(), re.MULTILINE).group(1)

setup(name='azuresshconfig',
    version=version,
    description='Generate SSH config file from Azure ARM VM inventry in subscription',
    long_description=long_description,
    author='Yoichi Kawasaki',
    author_email='yoichi.kawasaki@outlook.com',
    url='https://github.com/yokawasa/azure-ssh-config',
    platforms='any',
    license='MIT',
    py_modules=['azuresshconfig'],
    entry_points={
        'console_scripts': 'azuresshconfig=azuresshconfig:main',
    },
    install_requires=[
        'argparse',
        'simplejson',
        'msrestazure',
        'azure-mgmt-resource>=0.30.0rc6',
        'azure-mgmt-compute>=0.30.0rc6',
        'azure-mgmt-network>=0.30.0rc6'
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    keywords='azure ssh config',
)
