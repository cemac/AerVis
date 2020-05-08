'''
The First Level of the AerVis code.

This in essence perfoms a level of concatenation of the pp output of a model run, and parses them for plotting (as well as converts them into the netCDF file format).

UKCA format is generally in the form of `<filename>.pn<daily|monthly|yearly avarages>.pp`.

To run `python -m AerVis.L0 <args>`

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
'''

#glob imports
import sys,time,iris,datetime,getpass,os
import numpy as np
from glob import glob

#lib imports
from .ppread import *
from ..variable_dict import *


__all__ = '__OUTPUT_DIR__ __OROGRAPY__ rotate_cube lat lon run'.split()


__OROGRAPY__ = os.getenv('OROGRAPHY',os.getcwd()+'/n96_hadgem1_qrparm.orog_new.pp')
__OUTPUT_DIR__ = os.getenv('OUTPUTS',os.getcwd()+'/outputs')
#print(sys.argv,os.getcwd(),'dsf',__file__)
#os.getcwd()+

try:os.mkdir(__OUTPUT_DIR__)
except PermissionError: sys.exit('You do not have permissions to write in: '+ __OUPUT_DIR__+'. Exectured from: '+ os.cwd())
except OSError:None

rotate_cube=False
''' rotate the variable coordinates by the values of lat and lon within the L0 module'''
lat,lon = [0.0,0.0]
''' lat and lon variable values '''

def run(name:str,loc:str='./'):
    '''
    Default L0 run script for manual initiation, or being run as a module
    '''

    from .pprun import read_all,get_names

    # for __FILE__ in files
    __FILE__ = get_names(name,path=loc)
    __origin__ = name




    cubes=iris.load([__OROGRAPY__,__FILE__])
