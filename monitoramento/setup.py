from setuptools import setup, find_packages

setup(
    name="monitoramento",
    version="1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "streamlit",
        "plotly",
        "pandas",
        "python-dotenv",
        "SQLAlchemy",
        "pymysql",
    ],
)
