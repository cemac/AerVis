'''
The First Level of the AerVis code.

This in essence perfoms a level of concatenation of the pp output of a model run, and parses them for plotting (as well as converts them into the netCDF file format).

UKCA format is generally in the form of `<filename>.pn<daily|monthly|yearly avarages>.pp`.

'''

#glob imports
import sys,time,iris,datetime,getpass,os
import numpy as np
from glob import glob

#lib imports
from .ppread import *
from ..variable_dict import *


__all__ = ['__OUTPUT_DIR__','__OROGRAPY__']


__OROGRAPY__ = os.getenv('OROGRAPHY',os.getcwd()+'/n96_hadgem1_qrparm.orog_new.pp')
__OUTPUT_DIR__ = os.getenv('OUTPUTS',os.getcwd()+'/outputs')
#print(sys.argv,os.getcwd(),'dsf',__file__)
#os.getcwd()+

try:os.mkdir(__OUTPUT_DIR__)
except PermissionError: sys.exit('You do not have permissions to write in: '+ __OUPUT_DIR__+'. Exectured from: '+ os.cwd())
except OSError:None
