from os import path as ospath
import io
from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.md") as changelog_file:
    changelog = changelog_file.read()

pathdirname = ospath.abspath(ospath.dirname(__file__))

with io.open(ospath.join(pathdirname, "requirements.txt"), encoding="utf-8") as file:
    all_requirement = file.read().split("\n")

install_requirement = [x.strip() for x in all_requirement if "git+" not in x]
link_dependcy = [
    x.strip().replace("git+", "") for x in all_requirement if "git+" not in x
]
requirement = ["Click>=7.0"]

setup(
    name="bgis",
    description=str(readme),
    changelog=str(changelog),
    version="1.0.0",
    python_requires=">=3.10",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Indonesian",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    author="bellshade wpu",
    packages=find_packages(),
    project_urls={
        "Bug Reports": "https://github.com/bellshade/bgis/issues",
        "Source": "https://github.com/bellshade/bgis",
    },
)
