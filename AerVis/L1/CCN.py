'''
Critical diameter calculations submodule
'''

def getCCN(dataset,ims):

    '''
    CCN

    This method works for k>0.2, sc<1%
    Petters, M. D., & Kreidenweis, S. M. (2007).
    A single parameter representation of hygroscopic growth and cloud condensation nucleus activity.
    Atmospheric Chemistry and Physics, 7(8), 1961–1971. doi:10.5194/acp-7-1961-2007
    '''


    print('--- calculating L1.CCN --')

    surface_tension_water = 0.0761 - 1.55e-4 * (dataset['temperature'].data  - 273.)#J m^-2 Nenes/Seinfeld
    Mw=0.018015#molecular weight of water kg/mol
    R=8.3144#Universal gas constant J mol-1 K-1
    pw=1000#Density of water  kg m-3

    A_kohler = 4. * Mw * surface_tension_water / ( R * dataset['temperature'].data  * pw )
    
    ## kappa mode
    
    kappa_weighted_per_mode={}
    for mode_name in ims.mode_names:
        index = ims.mode_names.index(mode_name)
        
        if ims.modesol[index]:
            
            for comp_name in ims.component_names:
                
                if 'vol_'+comp_name+'_'+mode_name in dataset.keys():
                    print ('kappa_weighted_per_mode',mode_name,comp_name)
                    contribution = dataset['vol_'+comp_name+'_'+mode_name]*ims.kappa[index] / dataset['vol_'+mode_name]
                    
                    try:kappa_weighted_per_mode[mode_name] += contribution # sum
                    except KeyError:kappa_weighted_per_mode[mode_name] = contribution
                    
                    

    for supersaturation in [0.1,0.2,0.5,1]:
        
        print ('ccn at supersaturation of:', supersaturation)
        
        CCN_per_mode={}
        CCN=0
        
        for mode_name in ims.mode_names:
            index = ims.mode_names.index(mode_name)
            if ims.modesol[index]:
                
                if mode_name not in kappa_weighted_per_mode:
                    print ('CCN no ', mode_name)
                    continue
                
                critical_diameter_per_mode = (4.*A_kohler**3 / (27. * kappa_weighted_per_mode[mode_name].data * np.log( 1 + supersaturation/100.)**2))**(1./3.)
                
                N = dataset['n_'+mode_name]
                rbar = dataset['rad_'+mode_name].data
                sigma = ims.sigma[index]
                
                Dcrit = critical_diameter_per_mode
                Dcrit = dataset['temperature'].copy()
                
                Dcrit.attrs['long_name'] = 'Critical_diameter_with_supersaturation_of_%1.4f'%(supersaturation)
                Dcrit.attrs['var_name'] = 'Dcrit_%1.4f'%(supersaturation)
                Dcrit.attrs['units'] = 'meter'
                
                #Rcrit = Dcrit / 2.
                #ukl.lognormal_cummulative(N,Rcrit,rbar,sigma)
                
                CCN += N - (N/2) * (1 + scipy.special.erf( np.log( (Dcrit/2) / rbar ) / np.sqrt(2) / np.log(sigma)))
                
                
        name = 'ccn'+str(supersaturation)
        dataset[name] = CCN
        dataset[name].attrs['long_name'] = 'Cloud_condensation_nuclei_at_a_supersaturation_of_%1.4f'%supersaturation
        dataset[name].attrs['var_name'] = name
        
    return dataset