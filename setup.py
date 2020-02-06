from setuptools import setup, find_packages
from mictools import __version__

long_description = """MICtools is an open source pipeline which combines the
TIC_e and MIC_e measures into a two-step procedure that allows to
identify relationships of various degrees of complexity in large datasets. TIC_e
is used to perform efficiently a high throughput screening of all the possible
pairwise relationships assessing their significance, while MIC_e is used to rank 
the subset of significant associations on the bases of their strength. Homepage:
https://github.com/minepy/mictools.
"""

setup(
    name='mictools',
    version = __version__,
    packages = find_packages(),
    description='MICtools',
    long_description=long_description,
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
        'matplotlib>=1.2.0',
        'statsmodels>=0.6.1',
        'minepy>=1.2'],
    entry_points='''
            [console_scripts]
            mictools=scripts.mictools_cmd:cli
        ''',
    include_package_data = True
)
