from setuptools import setup, find_packages




setup(
    name='DnsCryptPiHoleSetup',
    version='0.14',
    url='https://github.com/jmcgrath207/DnsCryptPiHoleSetup',
    license='MIT License',
    author='John McGrath',
    author_email='john.mcgrath207@gmail.com',
    description='DnsCrypt Setup for PiHole Raspberry Pi 3',
    python_requires=">=3.5",
    install_requires=['Fabric3==1.13.1.post1','Click==6.7','click-help-colors==0.4'],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=False,
    entry_points={
        'console_scripts': [
            'DnsCryptPiHoleSetup=DnsCryptPiHoleSetup.DnsCryptPiHoleSetup:cli',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
)

