'''
Particular Matter calculations submodule
'''


def getPM(dataset,ims):

    print('--- calculating L1.PM (2.5 & 10) --')
    
    r_125 = 1.25e-6 #meters long_name='Radius for calculating PM2.5'   
    r_5   = 5e-6 #meters long_name='Radius for calculating PM10',
    r_5   = 5e-6  #meters long_name='Radius for calculating PM10',
    
    ## x38 - x
    for mode_name in ims.mode_names:
            #print mode_name
            try:
                
                Mode_mass = dataset['mcon_'+mode_name]
                N = dataset['n_'+mode_name]
                rbar = dataset['rad_'+mode_name].data
                sigma = ims.sigma[ims.mode_names.index(mode_name)]
                rbar_volume = rbar * np.exp( 3.0*np.log(sigma)**2 )

                # particle
                for name , r in [['N2p5',r125] , ['N10',r5]]:
                    
                    contribution = (N/2) * (1 + scipy.special.erf( \
                    np.log(r / rbar) / np.sqrt(2) / np.log(sigma)) )

                    try:dataset[name] += contribution # sum
                    except KeyError:dataset[name] = contribution
                                    
                
                #mass 
                for name , r in [['PM2p5',r125] , ['PM10',r5]]:
                    
                    contribution = (Mode_mass/2) * (1 + scipy.special.erf( \
                    np.log(r / rbar) / np.sqrt(2) / np.log(sigma)) )

                    try:dataset[name] += contribution # sum
                    except KeyError:dataset[name] = contribution
                    
                    
                #N total    
                try:dataset['Ntot'] += N # sum
                except KeyError:dataset['Ntot'] = N
                
                #Mass total    
                try:dataset['Mtot'] += Mode_mass # sum
                except KeyError:dataset['Mtot'] = Mode_mass
                
                
                
                

            except KeyError:
                print('missing:', mode_name)
                continue

    if 'PM2p5' in dataset:                      
        dataset['PM2p5'].attrs['var_name'] = 'PM2p5'
        dataset['PM2p5'].attrs['long_name'] = 'Mass_of_particules_smaller_than_a_diameter_of_2.5_um'
    
    if 'PM10' in dataset:      
        dataset['PM10'].attrs['var_name'] = 'PM10'
        dataset['PM10'].attrs['long_name'] = 'Mass_of_particules_smaller_than_a_diameter_of_10_um'
    
    if 'N2p5' in dataset:      
        dataset['N2p5'].attrs['var_name'] = 'N2p5'
        dataset['N2p5'].attrs['long_name'] = 'Particules_smaller_than_a_diameter_of_2.5_um'
    
    if 'N10' in dataset:      
        dataset['N10'].attrs['var_name'] = 'N10'
        dataset['N10'].attrs['long_name'] = 'Particules_smaller_than_a_diameter_of_10_um'
    
    if 'Mtot' in dataset:      
        dataset['Mtot'].attrs['var_name'] = 'Mtot'
        dataset['Mtot'].attrs['long_name'] = 'Total_mass_concentration'
    
    if 'Ntot' in dataset:      
        dataset['Ntot'].attrs['var_name'] = 'Ntot'
        dataset['Ntot'].attrs['long_name'] = 'Total_particle_concentration'
        
    return dataset
