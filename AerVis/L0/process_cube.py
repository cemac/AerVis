'''
A function to convert a cube into an xarray object and save it in a single dataset

'''
import xarray

def cube2xarr(cube:str,var_ref, stash_list:list=False,rotate_lat:float=0, rotate_lon:float=0):
    '''
    ---------------------------
    The first Level 0 function.
    ---------------------------

    This takes an iris cube - generated from a single pp file -  and creates a separate netcdf file for each property and each timestep.
    '''


    stash_code = str(cube.attributes['STASH']) # get __str__ from class

    if stash_list: # if a specified selection of stash codes is given use those
        if stash_code not in stash_list:
            return None


    if hasattr(var_ref,stash_code):

        if not isinstance(cube.long_name,str):
            cube.long_name=getattr(var_ref,stash_code)['long_name']

            if not isinstance(cube._var_name,str):
                if not getattr(var_ref,stash_code)['short_name']=='':
                    cube._var_name=getattr(var_ref,stash_code)['short_name']

        if rotate_lat: cube.coord('grid_latitude').points=cube.coord('grid_latitude').points+lat
        if rotate_lon: cube.coord('grid_longitude').points=cube.coord('grid_longitude').points+lon+180

    xr = xarray.DataArray.from_iris(cube)

    return [stash_code,xr]
