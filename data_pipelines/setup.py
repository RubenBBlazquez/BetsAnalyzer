import setuptools

# Read the contents of your requirements file
with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

setuptools.setup(
    name="data_pipelines",
    version="0.0.1",
    author="",
    author_email="",
    description="A package for data ETL pipelines",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=required_packages,
)
