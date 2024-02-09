from setuptools import setup, find_packages

setup(
    name='meu_chatbot',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'chatterbot',
    ],
    entry_points={
        'console_scripts': [
            'meu_chatbot_script = meu_chatbot:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
