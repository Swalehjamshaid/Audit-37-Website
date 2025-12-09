# File: setup.py ← NEW FILE, create it now
from setuptools import setup, find_packages

setup(
    name="audit-37-website",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "gunicorn",
    ],
)
