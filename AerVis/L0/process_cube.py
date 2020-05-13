'''
A function to convert a cube into an xarray object and save it in a single dataset

'''
import xarray,time




def cube2xarr(cubez:str,var_ref, stash_list:list=False,rotate_lat:float=0, rotate_lon:float=0):
    '''
    ---------------------------
    The first Level 0 function.
    ---------------------------

    This takes an iris cube - generated from a single pp file -  and creates a separate netcdf file for each property and each timestep.
    '''
    
    dataset = False
    
    start = time.perf_counter()
    
    for cube in cubez:
        
        stash_code = str(cube.attributes['STASH']) # get __str__ from class

        if stash_list: # if a specified selection of stash codes is given use those
            if stash_code not in stash_list:
                print( '-- skipping -- :'+ stash_code )
                continue
                
        if hasattr(var_ref,stash_code):

            if not isinstance(cube.long_name,str):
                cube.long_name=getattr(var_ref,stash_code)['long_name']

                if not isinstance(cube._var_name,str):
                    if not getattr(var_ref,stash_code)['short_name']=='':
                        cube._var_name=getattr(var_ref,stash_code)['short_name']
        
            if rotate_lat: cube.coord('grid_latitude').points=cube.coord('grid_latitude').points+lat
            if rotate_lon: cube.coord('grid_longitude').points=cube.coord('grid_longitude').points+lon+180
        
        
        xr = xarray.DataArray.from_iris(cube)
        
        if dataset: dataset[stash_code]= xr
        else: dataset = xr.to_dataset(name=stash_code) 
        
    avg_delta = (time.perf_counter()-start)/len(cubez)
        
    print('---- END L0 ---')
    return dataset,avg_delta
