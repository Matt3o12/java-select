from setuptools import setup

setup(
    name = "java-select",
    version = "1.0.0a",
    description = "Command line script to easily switch a Java version.",
    author = "Matteo Kloiber (Matt3o12)",
    author_email = "info@matt3o12.de",

    entry_points = {'console_scripts': "java-select = bin/java-select.py"},
)