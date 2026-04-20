from setuptools import setup

setup(
    name="Eugenia",
    version="1.0.0",
    packages=["core", "data", "utils", "models", "nucleus", "renderers", "extractors"],
    package_dir={"": "src"},
    url="https://github.com/Nearbe/Eugenia",
    license="LICENSE.md",
    author="Nearbe",
    author_email="e@nearbe.ru",
    description="Part of the Process",
)
