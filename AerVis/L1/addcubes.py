''' 
Function for multiprocessing the creation of cubes
'''


## particulates
def add_cube(info:dict):
    '''
    info - a dictionary of three values {name,longname,dataset,rval,cubes}
    Rval #meters long_name='Radius for calculating PM2.5',
    var_name='PM25'
    long_name='Mass_of_particules_smaller_than_a_diameter_of_2.5_um'
    cubes
    '''
    locals().update(d)

    dcubes_to_add_PM25=[]
    #meters long_name='Radius for calculating PM2.5',
    for mode_name in ims.mode_names:
        #print mode_name
        Mode_mass=mass_concentration_per_mode['mcon_'+mode_name]
        rbar=mode_radius['rad_'+mode_name].data
        sigma=ims.modal_attributes[mode_name].sigma
        rbar_volume=rbar*np.exp(3.0*np.log(sigma)**2)
        contribution_to_PM25=ukl.lognormal_cummulative(Mode_mass,r_125,rbar_volume,sigma)
        cubes_to_add_PM25.append(contribution_to_PM25)
    PM25=np.sum(cubes_to_add_PM25)

    save_cube(PM25)
    
    