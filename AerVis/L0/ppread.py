'''
Tools to read a number of pp files.
'''

import iris,glob

__all__ = 'get_names read_all'.split()


def get_names(name:str, path: str='./'):
    '''
    glob match of relevant files.
    Searches for the format <name>.pn<date>.pp
    '''
    if path[-1]!='/': path+='/'
    return glob.glob(path+name+'.pn*.pp')



def read_all(names: list, orography:str=False, savename: str=False):
    '''
    A funciton that can read all pp files into memory at once

    If savenc is given, the concatenated file is saved with the name proided and the '.nc' suffix appended.

    Names can be a list of files or a single element list containing a wildcard match (`myfile/pn*.pp`).
    '''

    if orography: files = [orography]
    else: files=[]

    files.extend(names)

    data = iris.load(files)

    if savename:
        print(savename,'\nsaving :',files)
        iris.save(data,savename.strip('.nc')+'.nc') #default is netcdf4

    return data
