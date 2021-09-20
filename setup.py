import pathlib
from distutils.core import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='ColabTurtlePlus',
    version='2.0',
    packages=['ColabTurtlePlus'],
    url='https://github.com/mathriddle/ColabTurtlePlus',
    license='MIT',
    author='Larry Riddle',
    author_email='lriddle@agnesscott.edu',
    description='An HTML based Turtle implementation for Google Colab and Jupyter Labs',
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
