from setuptools import setup, find_packages

setup(
    name='projeto-analise-dados',
    version='1.0.0',
    author='Seu Nome',
    author_email='seu_email@example.com',
    description='Projeto de análise de dados',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
    ],
)