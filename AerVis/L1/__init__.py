'''
The L1 section of the AerVis code

This section gathers information about the simulation runs
'''
from . import I_MODE_SETUP_var as imv #this seems to percist, but vars can be supplied separately if not the case. 


def run(self,save=True):
    
    
    # TEMPERATURE
    
    ''' Temperature '''
    if self.model == 'tomcat': self.temperature = self.data['m01s16i004'][0] ## temp
    else: pT = self.data['m01s00i004'][0] ## potential temp
        

    ''' AIR Pressure '''
    try:
        self.air_pressure=self.data['m01s00i408'][0]
        if self.air_pressure.shape != self.temperature.shape:
                    raise NameError('air pressure with different shape as potential_temperature')

    except NameError:
        ''' this will fall over''' 
        # air_pressure_nodim = self.data['m01s00i255'][0]
        # p_convert = iris.coords.AuxCoord(100000.0,
        #                           long_name='convert_units',
        #                           units='Pa')
        self.air_pressure=self.data['m01s00i255'][0]*100000.0


    '''
    TOMCAT TEMP
    p0= 100000 # 1 hPa = 100 Pa 
    Rd=287.05 # J/kg/K
    cp=1005.46 # J/kg/K
    '''
    if self.model != 'tomcat':self.temperature=pT*(self.air_pressure/100000.0)**(287.05/1005.46)
        
        
        
    ''' Air Density '''
    
    
    
    self.air_density=(self.air_pressure/(self.temperature*R_specific))





    self.particle_density_of_air=self.air_density/molar_mass_air*avogadro_number

    # ukl.#print_cube_single_value(particle_density_of_air) # Do not remove
    # 
    # 
    # 
    # air_density._var_name='air_density'
    # air_density.long_name='Density of air'
    # save_cube(air_density)
    # 
    # 
    
    ###########################################
    
    
    '''
    Add info
    '''
    
    
    self.vd()
    dataset = xarray.Dataset()
    
    # mass mixing ratios - particles concentration
    for entry in self.vr.match('nbr'):
        try:
            item = self.vr.get(entry)
            stash = item['stash_code']
            name = 'n'+stash[3:]
            
            new[name]=self.data[stash]*self.particle_density_of_air
            new[name].long_name='number_concentration'+ item['long_name'][15:]
            new[name]._var_name=name
            
        except KeyError :
            print(entry, ' not found!' )
            
    
    # mass mixing ratios - mass concentration    
    mc_keys = []    
    for entry in self.vr.match(['mmr','sol']) + self.vr.match(['mmr','ins']):
        try:
            item = self.vr.get(entry)
            stash = item['stash_code']  
            name = 'mcon_'+stash[3:]  
            
            new[name]=self.data[stash]*self.air_density
            new[name].long_name='mass_concentration'+ item['long_name'][13:-7]
            new[name]._var_name=name    
            
            mc_keys.append(name)
            
        except KeyError :
            print(entry, ' not found!' )
                        
    
    
    '''
    ims fn
    '''
    
    #mass_concentration_per_component
    for comp_name in ims.component_names:
        name = 'mcon_'+comp_name

        new[name].long_name='total_mass_concentration_of_%s'%comp_name
        new[name]._var_name=name
        
        for key in list(filter(lambda x: mode_name in x , mc_keys)):
            try:new[name]+=new[key]
            except:new[name]=new[key]
            

    #mass_concentration_per_mode
    for mode_name in ims.mode_names:
        name = 'mcon_'+mode_name

        new[name].long_name='total_mass_concentration_in_%s'%mode_name
        new[name]._var_name=name
        
        for key in list(filter(lambda x: mode_name in x , mc_keys)):
            try:new[name]+=new[key]
            except:new[name]=new[key]

        
    
    
    
    # 
    # 
    # mass_concentration_per_mode={}
    # for mode_name in ims.mode_names:
    #     cubes_to_add=[mass_concentration[key] for key in mass_concentration.keys() if mode_name in key]
    # 
    #     mass_concentration_per_mode['mcon_'+mode_name]=np.sum(cubes_to_add)
    #     mass_concentration_per_mode['mcon_'+mode_name].long_name='total_mass_concentration_in_%s'%mode_name
    #     mass_concentration_per_mode['mcon_'+mode_name]._var_name='mcon_'+mode_name
    #     save_cube(mass_concentration_per_mode['mcon_'+mode_name])

    # mass_concentration_per_component={}
    # for comp_name in ims.component_names:
    #     cubes_to_add=[mass_concentration[key] for key in mass_concentration.keys() if comp_name in key]
    #     mass_concentration_per_mode['mcon_'+comp_name]=np.sum(cubes_to_add)
    #     mass_concentration_per_mode['mcon_'+comp_name].long_name='total_mass_concentration_of_%s'%comp_name
    #     mass_concentration_per_mode['mcon_'+comp_name]._var_name='mcon_'+comp_name
    #     save_cube(mass_concentration_per_mode['mcon_'+comp_name])
'''

    #Calculate volume of modes per component
    mode_volume_per_component={}
    list_volumes=[]
    for mode_name in ims.mode_names:
        keys=[key for key in mass_concentration.keys() if mode_name in key]
        #print keys
        for comp_name in ims.component_names:
            keys_comp=[key for key in keys if comp_name in key]
            if len(keys_comp):
                mode_volume_per_component['vol_'+keys_comp[0][5:]]= \
                mass_concentration[keys_comp[0]]/ims.species_attributes[comp_name].rhocomp
                mode_volume_per_component['vol_'+keys_comp[0][5:]].long_name='Volume_fraction'+mass_concentration[keys_comp[0]].long_name[18:]
                mode_volume_per_component['vol_'+keys_comp[0][5:]]._var_name='vol_'+keys_comp[0][5:]
                save_cube(mode_volume_per_component['vol_'+keys_comp[0][5:]])

    #%%
    #Calculate volume and radius of modes
    mode_radius={}
    mode_volume={}

    for mode_name in ims.mode_names:
        keys=[key for key in mode_volume_per_component.keys() if mode_name in key]
        print mode_name

        cubes_to_add=[mode_volume_per_component[key] for key in keys]
        mode_volume['vol_'+mode_name]=np.sum(cubes_to_add)
        mode_volume['vol_'+mode_name]._var_name='vol_'+mode_name
        mode_volume['vol_'+mode_name].long_name='Total_volume_fraction_'+mode_name
        save_cube(mode_volume['vol_'+mode_name])

        mode_radius['rad_'+mode_name]=0.5*iris.analysis.maths.exponentiate((
            6*mode_volume['vol_'+mode_name]/particles_concentration['n_'+mode_name]
            )/(np.pi*np.exp(4.5*(np.log(ims.modal_attributes[mode_name].sigma))))
            ,1./3.)


        mode_radius['rad_'+mode_name]._var_name='rad_'+mode_name
        mode_radius['rad_'+mode_name].long_name='Radius_of_mode_'+mode_name
        save_cube(mode_radius['rad_'+mode_name])

        '''
        
'''
    filter nbr 
    filter mmr
    '''