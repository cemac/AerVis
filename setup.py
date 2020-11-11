import sys
print(sys.version)
if int(sys.version.split('.')[0]) < 3 :
    sys.exit('please use python 3') 

try:
    from setuptools import setup
except:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
'''
conda install -c conda-forge nco
'''    
req = 'dill datetime dask>=2.17.2 xarray scipy'.split()
req.append('iris @ https://github.com/SciTools/iris/archive/v2.4.0.tar.gz')
print('requirements: ',req)

setup(
    name="AerVis", # Replace with your own username
    version="0.0.2",
    author="CEMAC",
    # package_dir={'': 'AerVis'},
    # packages=setuptools.find_packages(where='AerVis'),
    packages = ['aervis'],
    author_email="K.Pringle(at)leeds.ac.uk,D.Ellis(at)leeds.ac.uk,eejvt(at)leeds.ac.uk",
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
    install_requires=req
)

#/opt/anaconda3/lib/python3.7/site-packages/aervis.egg-link

print('For advanced utilities please install netCDF Operator (NCO) http://nco.sourceforge.net')
'''
conda install -c conda-forge nco
'''    
