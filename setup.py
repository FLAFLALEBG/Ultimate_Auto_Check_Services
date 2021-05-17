from setuptools import setup

setup(
    name='uacs',
    version='0.3.15',
    description='This script allows to check services under Linux and sends mails in case of crash of one of them.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Flavio',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Natural Language :: French',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
    ],
    keywords="service monitoring",
    author_email='flaviocomblez@gmail.com',
    url='https://github.com/FLAFLALEBG/Ultimate_Auto_Check_Services',
    packages=['uacs'],
    install_requires=[
        'setuptools~=56.2.0'
    ],
    entry_points={
        'console_scripts': [
            'uacs = uacs.uacs:main'
        ],
    }
)
