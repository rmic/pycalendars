import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycalendars", # Replace with your own username
    version="0.0.1",
    author="Raphael Michel",
    author_email="raph.mic@gmail.com",
    description="A simple library to access your online calendars",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rmic/pycalendars",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)