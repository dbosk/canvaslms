from setuptools import setup, find_packages

setup(
    name = "canvaslms",
    version = "1.2",
    author = "Daniel Bosk",
    author_email = "dbosk@kth.se",
    description = "Command-line interface for Canvas LMS",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/dbosk/canvaslms",
    project_urls = {
        "Bug Tracker": "https://github.com/dbosk/canvaslms/issues",
        "Releases": "https://github.com/dbosk/canvaslms/releases"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Utilities"
    ],
    package_dir = {"": "src"},
    packages = ["canvaslms"],
    entry_points = {
        "console_scripts": [
            "canvaslms = canvaslms.cli:main"
        ]
    },
    data_files = [
        ("/etc/bash_completion.d", ["canvaslms.bash"])
    ],
    python_requires = ">=3.8",
    install_requires = [
        "appdirs>=1.4.4",
        "argcomplete>=1.12.3",
        "canvasapi>=2.0.0",
        "pypandoc>=1.6.4"
    ]
)
