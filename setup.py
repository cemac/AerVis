import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aervis", # Replace with your own username
    version="0.0.1",
    author="CEMAC",
    author_email="K.Pringle@leeds.ac.uk,D.Ellis(at)leeds.ac.uk,eejvt@leeds.ac.uk",
    description="A package for processing aerosol model output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/wolfiex/AerVis",
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords='aerosol cemac leeds ukca',
    package_dir={'': 'AerVis'},
    packages=find_packages(where='src'),
    install_requires='dill datetime xarray scipy https://github.com/SciTools/iris/releases/tag/v2.4.0'.split()
    
)