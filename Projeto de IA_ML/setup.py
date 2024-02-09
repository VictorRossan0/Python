from setuptools import setup, find_packages

setup(
    name='projeto-ia-ml',
    version='1.0.0',
    author='Seu Nome',
    author_email='seu_email@example.com',
    description='Projeto de IA/ML',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'tensorflow',
        'numpy',
    ],
)