import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="degit",
    version="0.0.1",
    author="Royinx, Thomas, Alex",
    author_email="",
    description="de-centrailized git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lchalex/MSBD5017_project",
    project_urls={
        "Bug Tracker": "https://github.com/lchalex/MSBD5017_project/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points={"console_scripts": ["degit = degit.main:main"]},
    include_package_data=True
    # data_files=[('src/degit/compiled_contracts',
    #              ['src/degit/compiled_contracts/*.json',
    #               'src/degit/compiled_contracts/*.txt'])]
)