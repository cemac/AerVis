# -*- coding: utf-8 -*-
'''
Variable Dictionary files
'''

import iris,re
# relative import ..
from ..global_config import __FILE_STASHmaster__,__FILE_PRESM_A_Summary__,__FILE_mapping__,__FILE_STASH_From_UMUI__
from .var_classes import *
import numpy as np



var_ref = VariableReference()


# stash_code='empty'
# long_name_mapping_file='long_name'
# name_mapping_file='name'
# units_mapping_file='units'
#
# name = 'empty'
# short_name='empty'
# long_name='empty'
# units='empty'

###############

with open(__FILE_STASHmaster__, 'r') as f:
    for _ in range(12):next(f) #skip 12

    #filter lines starting with 1
    stashdata = np.array(re.findall(r'\n1(%s)_*\|([^\|]+)'%(r'_*\|_*(\d+)'*3),re.sub('[ \t]+','_','\n'+f.read())))[:,1:]

    #parse the names and strip end space
    stashdata[:,-1] = np.vectorize(lambda x:x.strip('_').replace('/','div'))(stashdata[:,-1])

    # find codes which need a zero prebuffer for code nav
    stashdata[:,:2] = np.vectorize(lambda x: x.zfill(2))(stashdata[:,:2])

    stashdata[:,2] = np.vectorize(lambda x: x.zfill(3))(stashdata[:,2])


    for st1,st2,st3,name in stashdata:
        # add to reflist
        st_code='m'+st1+'s'+st2+'i'+st3
        var_ref.add({'stash_code':st_code,'name':name})

    # cleanup
    del stashdata,st1,st2,st3,name,st_code


####################


with open(__FILE_STASH_From_UMUI__) as f:
# Read first 8 lines as header.  There must be a better way to do this!
    for _ in range(8):next(f)

    #umui_table={}
    umui_table={'stash':[],'name':[]}

    for section,item,name in re.findall(r'\n\s*(\d+)\s*(\d+)\s*([^\n]+)','\n'+f.read()):
        umui_table['stash'].append(iris.fileformats.pp.STASH('1',section,item))
        umui_table['name'].append(name.strip().replace(' ','_'))

    del section,item,name


####################

#mapping_file_dict={'stash':[],'short_name':[],'long_name':[],'units':[]}

with open(__FILE_mapping__) as f:
    next(f)

    match = '([^\s]+)\s+'*4
    match = '\s*%s*\n'%(match[:-1])

    data = np.array(re.findall(match,f.read()))

#
# data = np.loadtxt(__FILE_mapping__,dtype=str,delimiter=' ',skiprows=1)

    stash = data[:,0]
    short_name = data[:,1]
    long_name = data[:,2]
    units = data[:,3]

    mapping_file_dict = dict(( (i,globals()[i]) for i in 'stash,short_name,long_name,units'.split(',')))

    for stash,short_name,long_name,units in data:
        var_ref.add(dict(( (i,globals()[i]) for i in 'stash,short_name,long_name,units'.split(','))))

    del data,stash,short_name,long_name,units,match



'''
gen stash picker
'''



#######################

print('fi::VariableDictionary')
