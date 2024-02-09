from setuptools import setup, find_packages

setup(
    name='projeto-web',
    version='1.0.0',
    author='Seu Nome',
    author_email='seu_email@example.com',
    description='Projeto de desenvolvimento web',
    packages=find_packages(),
    install_requires=[
        'flask',
        'sqlalchemy',
        'requests',
    ],
)