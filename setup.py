from setuptools import setup

setup(
    name='DnsCryptPiHoleSetup',
    version='1',
    packages=['CsvService', 'FabricService'],
    url='https://github.com/jmcgrath207/DnsCryptPiHoleSetup',
    license='MIT License',
    author='John McGrath',
    author_email='john.mcgrath207@gmail.com',
    description='DnsCrypt Setup for PiHole Raspberry Pi 3',
    python_requires=">=3.5",
    install_requires=['Fabric3==1.13.1.post1',],
)
