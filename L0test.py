# conda install -c conda-forge iris


import sys,time,iris,datetime,getpass,os
# import pathos as mp
# # sys.path.append(dir_scripts)
# import UKCA_lib as ukl
import numpy as np
from scipy.io import netcdf
from glob import glob
from AerVis.variable_dict import *


__OROGRAPY__ = os.getenv('OROGRAPHY','../n96_hadgem1_qrparm.orog_new.pp')
__OUTPUT_DIR__ = os.getenv('OUTPUTS','../outputs')
#os.getcwd()+

try:os.mkdir(__OUTPUT_DIR__)
except PermissionError: sys.exit('You do not have permissions to write in: '+ __OUPUT_DIR__+'. Exectured from: '+ os.cwd())
except OSError:None



# for __FILE__ in files
__FILE__ = 'bk417a.pn2008feb.pp'
__origin__ = __FILE__.strip('.pp')


stashcodes=set()
step_folders = set()

'''
if stash_list provided
stashcodes=stashlist
'''


rotate_cube=False
lat,lon = [0.0,0.0]

cubes=iris.load([__OROGRAPY__,__FILE__])


'''
Memory consumption:
4 pp files 500mb each ~2GB
500mb in memory python read
1.54GB .nc file compression.
'''

def pp2nc_single_var_ts(cube,stash_list=False):
    '''
    ---------------------------
    The first Level 0 function.
    ---------------------------

    This takes an iris cube - generated from a single pp file -  and creates a separate netcdf file for each property and each timestep.

    '''


    stash_code = str(cube.attributes['STASH']) # get __str__ from class

    if stash_list: # if a specified selection of stash codes is given use those
        if stash_code not in stash_list: continue



    stashcodes.add(stash_code)

    if hasattr(var_ref,stash_code):

        if not isinstance(cube.long_name,str):
            cube.long_name=getattr(var_ref,stash_code)['long_name']

            if not isinstance(cube._var_name,str):
                if not getattr(var_ref,stash_code)['short_name']=='':
                    cube._var_name=getattr(var_ref,stash_code)['short_name']


        times=cube.coord('time').points

        #########################################
        print("cube.long_name= "+str(cube.long_name))
        print("times= "+str(times))
        #########################################

        if rotate_cube:
            cube.coord('grid_latitude').points=cube.coord('grid_latitude').points+lat
            cube.coord('grid_longitude').points=cube.coord('grid_longitude').points+lon+180

        for time in times:
            # KP_Comment:  Extract / Constraint command failed if only 1 timestep as unbounded, added except statement below. 12/12/2018

            #########################################
            folder_NETCDF= '%s/%d/'%(__OUTPUT_DIR__,time)
            try:
                os.mkdir(folder_NETCDF)
                #os.chmod(folder_NETCDF, stat.S_IROTH)
            except OSError:None
            step_folders.add(folder_NETCDF)
            print("folder_NETCDF= "+str(folder_NETCDF))
            #########################################

            try:
                cube_single_t=cube.extract(iris.Constraint(time=time))
            except:
                '''
                Is this the correct action on failure - .extract documentation not found - de
                '''
                print("Cannot extract cube ",cube.long_name)
                print("Dimensions ",cube.shape)
                cube_single_t=cube


            if cube_single_t._standard_name:save_name='_'+cube_single_t._standard_name
            elif isinstance(cube.long_name,str): save_name='_'+cube_single_t.long_name
            else:save_name =''



            save_name='%(folder)spp2nc_%(stash)s_%(origin)s%(name).nc'%{'folder':folder_NETCDF,'stash':stash_code,'name':save_name,'origin':__origin__}

            #save_name = '%sfile_test.nc'%(folder_NETCDF,)


            print (folder_NETCDF,save_name)
            #https://github.com/SciTools/iris/issues/2919
            iris.save(cube_single_t, save_name, netcdf_format="NETCDF4")
            # with iris.fileformats.netcdf.Saver('test.nc', netcdf_format='NETCDF4') as sman:
            #     sman.write(cube_single_t)

#with Manager() as manager:





def join_variables(stash_list,step_folders):
    '''
    ---------------------------
    The second Level 0 function.
    ---------------------------

    This takes all the separately converted netcdf files and groups them for each timestep - as denoted by the directories in step_folders.

    '''

    # Generator filter removing orthography files
    stash_list = (i for i in stash_list if i != 'm01s00i033' )

    for stash_code in stash_list:

        # par here


        for step_folder in step_folders:

            '''
            name contains stash code
            glob files in folder
            '''
            file_name = glob('%(loc)spp2nc_%(stash)s*.nc'%{'loc':step_folder,'stash':stash_code})[0]

            # print(file_name)
            # if len(file_name)>=1:names.append(file_name[0])


            cube_list=iris.load(file_name)


            #https://scitools.org.uk/iris/docs/latest/userguide/merge_and_concat.html


            cube_list_concatenated=cube_list.concatenate()[0]

            if stash_code in vd.variable_reference_stash:
                if not isinstance(cube_list_concatenated.long_name,str):
                    cube_list_concatenated.long_name=vd.variable_reference_stash[stash_code].long_name
                    # print 'added long_name',cube_list_concatenated.long_name, 'to', stash_code

            # print cube_list_concatenated.standard_name
            if cube_list_concatenated.standard_name:
                saving_name=folder_all_time_steps+'All_time_steps_'+stash_code+'_'+cube_list_concatenated._standard_name+'.nc'
            elif isinstance(cube_list_concatenated.long_name,str):
                saving_name=folder_all_time_steps+'All_time_steps_'+stash_code+'_'+cube_list_concatenated.long_name+'.nc'
            else:
                saving_name=folder_all_time_steps+'All_time_steps_'+stash_code+'.nc'

            iris.save(cube_list_concatenated,saving_name, netcdf_format="NETCDF4")

            #########################################
            print("cube_list_concatenated="+str(cube_list_concatenated.long_name))

        del cube_list






##################
#part 1
##################

for cube in cubes[:5]:
    print('runnnnn')
    pp2nc_single_var_ts(cube)
stashcodes=list(set(stashcodes))
step_folders=list(set(step_folders))
step_folders.sort()


#print 'time to convert from pp to single nc:',end-start
''' does join join all pp files at start of program '''


##################
#part 2
##################

'''

Questions
iris save with same file name - what happens
concat on stash with same time. Is this across all possible pp files that are given? If there exist numtiple ones for each stash, only the first is taken. How does iris know?

different types of models - different scripts
can we automatically detect the origin model

control file = 3 using l0
only 2 on l1 - reason?


https://www.cloudcity.io/blog/2019/02/27/things-i-wish-they-told-me-about-multiprocessing-in-python/

>>> from pathos.pools import ProcessPool
>>> pool = ProcessPool(nodes=4)
>>>
>>> # do a blocking map on the chosen function
>>> results = pool.map(pow, [1,2,3,4], [5,6,7,8])
>>>
>>> # do a non-blocking map, then extract the results from the iterator
>>> results = pool.imap(pow, [1,2,3,4], [5,6,7,8])
>>> print("...")
>>> results = list(results)
>>>
>>> # do an asynchronous map, then get the results
>>> results = pool.amap(pow, [1,2,3,4], [5,6,7,8])
>>> while not results.ready():
...     time.sleep(5); print(".", end=' ')
...
>>> results = results.get()


'''



print('fi')
