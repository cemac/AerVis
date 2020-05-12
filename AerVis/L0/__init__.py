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
import sys,time,iris,datetime,getpass,os,xarray
import numpy as np
from glob import glob

#lib imports
from .ppread import *
from ..variable_dict import *
from .process_cube import *

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


def run(name:str,loc:str='./'):
    '''
    Default L0 run script for manual initiation, or being run as a module.

    Concatenates all files into an xarray Dataset rather than an iris cube list (the end result is the same exept this is cleaner.)

    '''


    # from .ppread import read_all,get_names

    # for __FILE__ in files
    __FILES__ = get_names(name,path=loc)
    __origin__ = name


    __FILES__.insert(0,__OROGRAPY__)

    print ('---- Loading %s ----'%name)
    start = time.perf_counter()
    cubes=iris.load(__FILES__)
    end = time.perf_counter() - start

    print (' %.2f minutes: %d files %d cubes'%(end/60,len(__FILES__),len(cubes)))


    return cube2xarr(cubes[0],var_ref=var_ref,rotate_lat=rotate_lat, rotate_lon=rotate_lon)
