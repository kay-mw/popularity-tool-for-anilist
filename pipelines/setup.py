from setuptools import find_packages, setup

setup(
    name="pipelines",
    packages=find_packages(exclude=["pipelines_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "SQLAlchemy",
        "pyodbc",
        "pandas",
        "azure-storage-blob",
        "python-dotenv",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
