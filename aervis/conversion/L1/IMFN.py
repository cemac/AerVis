''' 
Submodule for the Imode based functions
'''

def getIMFN(dataset,ims,mc_keys):
    
    print ('--- Calculating IMFN ---')
    
    #   mass_concentration_per_component
    for comp_name in ims.component_names:
        name = 'mcon_'+comp_name
        
        for key in list(filter(lambda x: comp_name in x , mc_keys)):
            try:dataset[name] += dataset[key] # sum
            except KeyError:dataset[name] = dataset[key]
        
        if hasattr(dataset,name):      
            dataset[name].attrs['long_name'] = 'total_mass_concentration_of_%s'%comp_name
            dataset[name].attrs['var_name'] = name
            print(name)
        else: print(name, 'skipped')
        


    #   mass_concentration_per_mode
    for mode_name in ims.mode_names:
        name = 'mcon_'+mode_name

        for key in list(filter(lambda x: mode_name in x , mc_keys)):
            try:dataset[name] += dataset[key]
            except:dataset[name] = dataset[key]
        
        if hasattr(dataset,name):      
            dataset[name].attrs['long_name'] = 'total_mass_concentration_in_%s'%mode_name
            dataset[name].attrs['var_name'] = name
            print(name)
        else: print(name, 'skipped')
        
        
        ## 196 - 209
        for comp_name in ims.component_names:
            keys_comp = list(filter(lambda x: comp_name in x , mc_keys))
            if len(keys_comp):
                name = 'vol_' + keys_comp[0][5:]
                
                dataset[name] = dataset['mcon_'+keys_comp[0]]/ims.rhocomp[ims.component_names.index(comp_name)]
                
                dataset[name].attrs['long_name'] ='Volume_fraction'+dataset[keys_comp[0]].attrs['long_name'][18:]
                
                dataset[name].attrs['var_name'] = name
                
                    

        ''' Volume '''        
                
    vol_keys = list(filter(lambda x: 'vol_' in x , dataset.keys()))  #mode_volume_per_component.keys() 
     
    for mode_name in ims.mode_names:
        
        # mode volume
        name = 'vol_'+mode_name
        
        for key in list(filter(lambda x: mode_name in x , vol_keys)):
            try:dataset[name] += dataset[key] # sum
            except KeyError:dataset[name] = dataset[key]
            
        if name in dataset.keys():    
            dataset[name].attrs['var_name'] = name
            dataset[name].attrs['long_name'] = 'Total_volume_fraction_'+mode_name



        # mode radius - equation should probably be rewritten (simplified)
        name = 'rad_' + mode_name
        
        try:
            dataset[name] = 0.5 * \
                ((6*dataset['vol_'+mode_name] / dataset['n_'+mode_name]) / \
                    (np.pi * np.exp( \
                        4.5*(np.log(ims.sigma[ims.mode_names.index(mode_name)]))**2) \
                    )) ** (1./3.)
                                 
            dataset[name].attrs['var_name'] = name
            dataset[name].attrs['long_name'] = 'Radius_of_mode_'+mode_name
            
        except KeyError:
            print('missing ',name)
            
            
    return dataset