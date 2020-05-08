'''
Global dictionary for AerVis
This contains the default locations of files required by the code.
These may be overwritten using a config file.

'''
import os
LIBLOC = __file__.strip('global_config.py')





# VarDict Files

# get location from env variable, or use default
VD_LOC = os.getenv('VDLOC', LIBLOC + 'variable_dict/' )

__FILE_STASHmaster__ = VD_LOC + 'STASHmaster_A'
__FILE_PRESM_A_Summary__= VD_LOC + 'PRESM_A_Summary_File.txt'
__FILE_mapping__ = VD_LOC + 'ukca_stdname_vn92_v2'
__FILE_STASH_From_UMUI__= VD_LOC + 'teafy.A.diags_short'
