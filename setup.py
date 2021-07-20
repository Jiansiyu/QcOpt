from setuptools import setup
import os

requirefile=os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
install_requires = [
    'cycler==0.10.0',
    'decorator==4.4.2',
    'kiwisolver==1.3.1',
    'matplotlib==3.4.2',
    'networkx==2.5.1',
    'numpy==1.21.1',
    'Pillow==8.3.1',
    'pyparsing==2.4.7',
    'python-dateutil==2.8.2',
    'PyYAML==5.4.1',
    'six==1.16.0',
    ]

if not install_requires and os.path.isfile(requirefile):
    with open(requirefile) as f:
        install_requires = f.read().splitlines()

setup(
    name='quantumc_optimizer',
    version='demo-0',
    description="Quantum Circuit Optimizer",
    author='Siyu Jian',
    author_email='sj9va@virginia.edu',
    packages=['quantumc_optimizer'],
    install_requires = install_requires
)