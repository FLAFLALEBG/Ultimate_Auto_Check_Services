import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='uacs',
    packages='uacs',
    version='0.1.1',
    url='https://github.com/FLAFLALEBG/Ultimate_Auto_Check_Services',
    license='GNU General Public License v2 (GPLv2) (GPL-2.0-only)',
    author='Flavio',
    author_email='flaviocomblez@gmail.com',
    description='This script allows to check services under Linux and sends mails in case of crash of one of them.',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8"
        "Programming Language :: Python :: 3.9",
    ],
    long_description=README,
)
