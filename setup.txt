from setuptools import setup

setup(
    name='Ultimate_Auto_Check_Servies',
    version='0.1',
    packages=['Ultimate_Auto_Check_Servies'],
    url='https://github.com/FLAFLALEBG/Ultimate_Auto_Check_Servies',
    license='GNU General Public License v2 (GPLv2) (GPL-2.0-only)',
    author='Flavio',
    keywords=['mail', 'automatic', 'service', 'monitor'],
    author_email='flaviocomblez@gmail.com',
    description='This script allows to check services under Linux and sends mails in case of crash of one of them.',
    classifiers=[
        'Development Status :: 3 - Alpha',  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: System administrator',
        'Topic :: System administration',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
