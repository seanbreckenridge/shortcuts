from pathlib import Path
from setuptools import setup


def main():

    setup(
        name="shortcuts",
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
        # install both as a script and a module
        py_modules=["shortcuts"],
        scripts=["shortcuts"],
        install_requires=Path("requirements.txt").read_text().strip().splitlines(),
        keywords="scripting",
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
