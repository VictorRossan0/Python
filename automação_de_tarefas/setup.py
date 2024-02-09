from setuptools import setup, find_packages

setup(
    name='projeto-automacao',
    version='1.0.0',
    author='Seu Nome',
    author_email='seu_email@example.com',
    description='Projeto de automação de tarefas',
    packages=find_packages(),
    install_requires=[
        'pyautogui',
        'schedule',
        'pandas',
    ],
)