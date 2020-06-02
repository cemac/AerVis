'''
The First Level of the AerVis code.

This in essence perfoms a level of concatenation of the pp output of a model run, and parses them for plotting (as well as converts them into the netCDF file format).

UKCA format is generally in the form of `<filename>.pn<daily|monthly|yearly avarages>.pp`.

To run the module use `python -m AerVis.L0 <args>`

 To run interactively:
<code>

     import airvis

     # update variables (e.g. rotate_cube)
     airvis.L0.rotate_cube = True
     airvis.L0.lat=10
     airvis.L0.lon=29

     # run
     airvis.L0.run('UKCArun','./runs/')
 </code>

Notes:
Speed is lost on IO, we want to minimise the amount of file reading and writing. LO functions have been concatenated.

Iris does not hold read files in memory, and can read from several at the same time using the netCDF or pp binary formats.


'''



#glob imports
import sys,time,iris,datetime,getpass,os,xarray,dill
import numpy as np
from glob import glob
from functools import partial
import multiprocessing as mp

#lib imports
from .ppread import *
from ..variable_dict import *
from .process_cube import *
from ..util import chunk
from ..global_config import __FILE_STASHmaster__,__FILE_mapping__,__FILE_STASH_From_UMUI__

__all__ = '__OUTPUT_DIR__ __OROGRAPY__ rotate_lat rotate_lon run'.split()


__OROGRAPY__ = os.getenv('OROGRAPHY',os.getcwd()+'/n96_hadgem1_qrparm.orog_new.pp')
__OUTPUT_DIR__ = os.getenv('OUTPUTS',os.getcwd()+'/outputs')
#print(sys.argv,os.getcwd(),'dsf',__file__)
#os.getcwd()+
try:os.mkdir(__OUTPUT_DIR__)
except PermissionError: sys.exit('You do not have permissions to write in: '+ __OUPUT_DIR__+'. Exectured from: '+ os.cwd())
except OSError:None

rotate_lat,rotate_lon = [0.0,0.0]
''' rotate the variable coordinates by the values of lat and lon within the L0 module'''






def run(name:str,loc:str='./',ncpu:int=4,__FILES__= False, stash_master=__FILE_STASHmaster__, stash_mapping=__FILE_mapping__, stash_umi=__FILE_STASH_From_UMUI__ , stashname = ''):
    '''
    Default L0 run script for manual initiation, or being run as a module.

    Concatenates all files into an xarray Dataset rather than an iris cube list (the end result is the same exept this is cleaner.)

    '''


    # from .ppread import read_all,get_names

    __origin__ = name
    if not __FILES__:__FILES__ = get_names(name,path=loc)
    # __FILES__ = __FILES__[:2]
    __FILES__.insert(0,__OROGRAPY__)
    
    

    print ('---- Loading %s ----'%name)
    start = time.perf_counter()
    cubes=iris.load(__FILES__)
    end = time.perf_counter() - start
    print (' %.2f minutes: %d files %d cubes'%(end/60,len(__FILES__),len(cubes)))

    
    
    if not stashname: stashname = '_'.join(stash_master,stash_mapping,stash_umi)
    try:#does a pickle already exist
        var_ref = dill.load(open(stashname+'.dl','rb'))  
    except FileNotFoundError:
        var_ref = makeVR(stashname)
        var_ref.save(stashname+'.dl')


    kwargs = {'var_ref':var_ref,'rotate_lat':rotate_lat, 'rotate_lon':rotate_lon}
    
    
    # 
    # 
    # pool = mp.Pool(ncpu)    
    # 
    # cube_list = pool.map_async( partial(cube2xarr,**kwargs), list(chunk(cubes,ncpu)) ) 
    # 
    # while not cube_list.ready():
    # 
    #     import sys
    # 
    #     chars = ".:':."
    # 
    #     for c in chars:
    #         sys.stdout.write(c)
    #         sys.stdout.write('\b')
    #         sys.stdout.flush()  
    #         time.sleep(1)
    # 
    #     time.sleep(3)
    # 
    # cube_list = np.array(cube_list.get())
    
    # data = xarray.combine_by_coords(cube_list[:,0])
    
    ## GET DATASET - multiprocessing crashes read of file
    
    
    
    
    data = cube2xarr(cubes, **kwargs)
    
    # data.attrs['avg_cube_delta']= cube_list[:,2].mean()
    data.attrs['files'] = __FILES__#','.join(__FILES__)
    total = time.perf_counter() - start
    data.attrs['iris_cube_delta'] = end
    data.attrs['L0_delta'] = total
    print (' ------- ',data.attrs['files'],data.attrs['avg_cube_delta'],total/60)
    
        
    # group 
    
    return data
    
