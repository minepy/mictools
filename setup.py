from setuptools import setup, find_packages
from mictools import __version__

setup(
    name='mictools',
    version = __version__,
    packages = find_packages(),
    description='MICtools',
    long_description=open('README.rst').read(),
    url='https://github.com/minepy/mictools',
    download_url='https://github.com/minepy/mictools/releases',
    license='GPLv3',
    author='Davide Albanese',
    author_email='davide.albanese@gmail.com',
    maintainer='Davide Albanese',
    maintainer_email='davide.albanese@gmail.com',
    install_requires=[
        'Click>=5.1',
        'numpy>=1.7.0',
        'scipy>=0.13',
        'pandas>=0.17.0',
        'matplotlib>=1.2.0,<2',
        'statsmodels>=0.6.1',
        'minepy>=1.2'],
    entry_points='''
            [console_scripts]
            mictools=scripts.mictools_cmd:cli
        ''',
    use_2to3 = True,
    include_package_data = True
)
