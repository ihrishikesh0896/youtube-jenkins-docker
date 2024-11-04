from setuptools import setup, find_packages

setup(
    name="text_analyzer",  # Note: using underscore instead of hyphen
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},  # This tells setuptools to look for packages in src directory
    install_requires=[],
    python_requires=">=3.7",
    author="Procrast.tech",
    description="A simple text analysis package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)