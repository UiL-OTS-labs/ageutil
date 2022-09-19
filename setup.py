import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ageutil",
    version="0.0.1",
    author="UiL OTS Labs",
    author_email="labbeheer.gw@uu.nl",
    description="Python library for age and birthday related calculations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UiL-OTS-labs/ageutil",
    packages=setuptools.find_packages(),
    license_files=('LICENSE',),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
