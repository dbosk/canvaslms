from setuptools import setup

with open("README.md", "r") as f:
  README = f.read()

setup(
    name="canvas-cli",
    version="0.1",
    description="Command-line interface to Canvas LMS",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dbosk/canvasy",
    author="Daniel Bosk",
    author_email="daniel at bosk dot se",
    py_modules=["canvas"],
    package_dir={"": "src"},
    classifiers=[
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.6",
      "Environment :: Console",
      "Operating System :: POSIX",
      "License :: OSI Approved :: MIT",
    ],
    install_requires=[
      "canvasapi ~= 2.0",
    ],
    extras_require = {
      "dev": [
        "pytest>=3.7",
      ],
    },
)
