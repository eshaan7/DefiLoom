import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

GITHUB_URL = "https://github.com/eshaan7/DefiLoom"

# Get requirements from files
requirements = (HERE / "requirements.txt").read_text().split("\n")
requirements_dev = (HERE / "requirements.dev.txt").read_text().split("\n")

# This call to setup() does all the work
setup(
    name="defiloom",
    version="0.0.1",
    description="A CLI tool that uses PowerLoom's DeFi API to discover Arbitrage and LP APY opportunities.",
    long_description=README,
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    author="Eshaan Bansal",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.10",
    include_package_data=True,
    install_requires=requirements,
    project_urls={
        "Documentation": GITHUB_URL,
        "Source": GITHUB_URL,
        "Tracker": "{}/issues".format(GITHUB_URL),
    },
    keywords="",
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev]
    extras_require={
        "dev": requirements_dev + requirements,
    },
    # pip install --editable .
    entry_points="""
        [console_scripts]
        defiloom=src.main:cli
    """,
)
