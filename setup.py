from setuptools import setup
import os

requirefile=os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
install_requires = []

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