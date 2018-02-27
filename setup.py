from setuptools import setup, find_packages
import codecs


def read_install_requirements():
    with codecs.open('./requirements.txt', 'r', encoding='utf8') as f:
        content = f.readlines()
        requirements = [line.strip('\n') for line in content]
    return requirements

setup(
    name="zzAutoPilot",
    version="0.0",
    packages=find_packages(),
    install_requires=read_install_requirements()
)