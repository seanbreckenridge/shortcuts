from pathlib import Path
from setuptools import setup, find_packages  # type: ignore[import]


def main():
    pkg = "shortcuts"

    setup(
        name=pkg,
        version="0.1.0",
        url="https://github.com/seanbreckenridge/shortcuts",
        author="Sean Breckenridge",
        author_email="seanbrecke@gmail.com",
        description=(
            "Creates arbitrary shell scripts from a configuration file; shortcuts"
        ),
        long_description=Path("README.md").read_text(),
        long_description_content_type="text/markdown",
        license="MIT",
        install_requires=Path("requirements.txt").read_text().strip().splitlines(),
        packages=find_packages(include=[pkg]),
        package_data={pkg: ["py.typed"]},
        python_requires=">=3.7",
        keywords="scripting",
        entry_points={"console_scripts": ["shortcuts = shortcuts.__main__:cli"]},
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
        ],
    )


if __name__ == "__main__":
    main()
