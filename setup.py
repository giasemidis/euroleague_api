from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='euroleague_api',
    version='0.0.1',
    author='Georgios Giasemidis',
    author_email='g.giasemidis@gmail.com',
    description='A Python wrapper of the Euroleague API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',
        'pandas',
        'numpy',
        'mypy',
        'pandas-stubs'
    ],
)
