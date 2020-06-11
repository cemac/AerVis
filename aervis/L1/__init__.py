'''
The L1 section of the AerVis code

This section gathers information about the simulation runs


args: 
    overwrite - ignores the fact L1 has already been run


testing:

import xarray,scipy
import numpy as np
from aervis.L1 import I_MODE_SETUP_var as ims 
from aervis.L1 import coords

'''

import xarray,scipy,time
import numpy as np

def run(self,imode:str = False,overwrite:bool=False ):
    '''
    The generic L1 function (for all files). 
    
    imode - full path including.py executable to I_MODE_SETUP_config
    '''
    
    start = time.perf_counter()
    
    if 'L1_variables' in self.data.attrs.keys() and not overwrite:
        print ('L1 has already been computed on this datset, skipping')
        return None
        
    
    
    from . import coords
    
    if imode: #import from filepath provided
        import importlib.util as ut 
        spec = ut.spec_from_file_location("module.name", imode)
        ims = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ims)
    else:    
        from . import I_MODE_SETUP_var as ims 


    self.vd() # generate variable dictionary  as this will be needed. 
    dataset = xarray.Dataset() # empty dataset
    dataset = coords.add(dataset) # add required constants to coordinates
    
#######################################################################    

    ''' Temperature '''
    if self.model == 'tomcat': 
        pT = self.data['m01s00i004'] #??potential_temperature
        tshape = pT.shape
    else:
        dataset['temperature'] = self.data['m01s16i004'] #[0]??
        tshape = dataset['temperature'].shape
        
        
#######################################################################    
    
    ''' AIR Pressure '''
    try:
        dataset['air_pressure'] = self.data['m01s00i408']
    
        if dataset['air_pressure'].shape != tshape:
                raise NameError('air pressure with different shape as potential_temperature ',dataset['air_pressure'].shape,tshape)
    
    
    except NameError or KeyError:
    #     # convert to Pa -> * 100000
         dataset['air_pressure'] = self.data['m01s00i255'][0]*100000.0 # 

#######################################################################    
# 
    if self.model == 'tomcat':dataset['temperature'] = pT*(dataset['air_pressure']/100000.0)**(287.05/1005.46)
        # p0 = 100000 # 1 hPa = 100 Pa 
        # Rd = 287.05 # J/kg/K
        # cp = 1005.46 # J/kg/K

#######################################################################            


    ''' Air Density '''

    dataset['air_density'] = (dataset['air_pressure']/(dataset['temperature']*dataset.coords['r_specific']))

    dataset['particle_density_air'] = dataset['air_density']/dataset.coords['molar_mass_air']*dataset.coords['avogadro']



#######################################################################    


    '''Additional info'''


    # mass mixing ratios - particles concentration
    for entry in self.vr.match('nbr'):
        try:
            item = self.vr.get(entry)
            stash = item['stash_code']
            name = 'n'+stash[3:]

            dataset[name] = self.data[stash]*dataset['particle_density_air']
            dataset[name].attrs['long_name'] = 'number_concentration'+ item['long_name'][15:]
            dataset[name].attrs['var_name'] = name

        except KeyError :
            print(entry, ' not found!' )


    # mass mixing ratios - mass concentration    
    # Calculate mass concentrations from air density and mass mixing ratios
    mc_keys = []    
    for entry in self.vr.match(['mmr','sol']) + self.vr.match(['mmr','ins']):
        try:
            item = self.vr.get(entry)
            stash = item['stash_code']  
            name = 'mcon_'+stash[3:]  

            dataset[name] = self.data[stash]*dataset['air_density']
            dataset[name].attrs['long_name'] = 'mass_concentration'+ item['long_name'][13:-7]
            dataset[name].attrs['var_name'] = name    

            mc_keys.append(name)

        except KeyError :
            print(entry, ' not found!' )








#######################################################################     

    '''Imode functions'''
    from . import IMFN
    dataset = IMFN.getIMFN(dataset,ims,mc_keys)

#######################################################################    

    ''' Particulate matter calculations '''
    from . import PM
    datset = PM.getPM(dataset,ims)


#######################################################################   

    ''' Critical Diameter '''                

    from . import CCN
    datset = CCN.getCCN(datset,ims)
    
    
        
#######################################################################           
    '''
    Update parameters from L1 and write to file
    L1 var = list 
    L1 coord = list
    L1 attr = List 
    '''
    
    dataset.attrs['L1_variables'] = ' '.join(dataset.keys())
    dataset.attrs['L1_attrs'] = ' '.join(dataset.attrs.keys())
    dataset.attrs['L1_coords'] = ' '.join(dataset.coords.keys())
    dataset.attrs['L1_delta_nowrite'] = time.perf_counter() - start
    
    
    
    self.data.close()
    
    ## append to netCDF
    try: dataset.to_netcdf(self.nc_loc,mode='a',format='NETCDF4',compute=True)
    
    except OSError as e:
        self.killreading()
        dataset.to_netcdf(self.nc_loc,mode='a',format='NETCDF4',compute=True)
        
    
    print('--- L1 finished ---',(time.perf_counter() - start)/60)
    return True #dataset # must return true if sucessful
    
    #python -c "import aervis; d = aervis.AerData('ACURE_PPE_001_bs714a');d.getL1(overwrite=True) "
