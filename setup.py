import os
import pathlib

import pkg_resources
from setuptools import find_packages, setup

requirements_txt = pathlib.Path("requirements.txt").read_text()
requirements = list(map(str, pkg_resources.parse_requirements(requirements_txt)))


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths


setup(
    name="sweeper",
    version="1.0.0-beta",
    packages=find_packages(),
    data_files=[("", package_files("src/data"))],
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sweeper = src.cli:cli",
        ],
    },
)
