from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyutils_generic", #Name
    version="0.1.0", #Version
    author="Ankit Kumar",
    author_email="ankit8290@gmail.com",
    description="Package to provide various practical python utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=None,
    packages = find_packages(include=["pyutils_generic", "pyutils_generic.*"]),   # Automatically find the packages that are recognized in the '__init__.py'.
    include_package_data=True,
    package_dir={"": "."},
    test_suite="pyutils_generic.tests",
    tests_require=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)