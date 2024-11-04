from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="text_analyzer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    python_requires=">=3.7",
    author="Procrast.tech",
    description="A simple text analysis package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)