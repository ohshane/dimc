from setuptools import setup, find_packages

setup(
    name="dimc",
    version="0.2.2",
    description="A utility for debugging dimensions of tensors and objects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Shane Oh",
    author_email="ohshane71@gmail.com",
    url="https://github.com/ohshane/dimc",
    packages=find_packages(),
    install_requires=["torch"],
    python_requires=">=3.7",
    license="BSD-3-Clause",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)