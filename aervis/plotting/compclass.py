from netCDF4 import Dataset as netcdf_dataset

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colorbar,colors,rcParams
rcParams['mpl_toolkits.legacy_colorbar'] = False
import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from mpl_toolkits.axes_grid1 import AxesGrid
import numpy as np

class AerComp():
    '''
    The plotting Class
    '''
    def __init__(self,base:str,peturbed:str):
        '''
        Arguments:
            base - the initial simulation path and filename
            peturbed - the changes simulation path and filename
            
            Both arguments require the full path to the netCDF file we wish to load.
        '''
        
        self.basename = base.split('/')[-1]
        self.base = netcdf_dataset(base)
        self.basevars = self.base.variables
        
        self.peturbedname = peturbed.split('/')[-1]
        self.peturbed = netcdf_dataset(peturbed)
        self.peturbedvars = self.base.variables
        
        self.varboth = set(self.basevars) & set(self.basevars)
        
        
    def diff_var(self):
        '''
        Return the different variables between each Dataset
        '''
        return list(self.varboth)
    
    def dims(self,stashcode:str):
        '''
        Retruns the dimensions of a stashcode variable
        '''
        return {'base':self.base.variables[stashcode].dimensions,
        'peturbed':self.peturbed.variables[stashcode].dimensions}
            
    def stashinfo(self, stashcode:str ):
        
        if stashcode not in self.varboth:
            print('Stashcode %s does not exist in both files')
            return None
        
        print('--- %s ---'%stashcode)
        print ('\tBASE (%s)'%self.basename)
        what = self.base.variables[stashcode]
        try: desc = what.long_name
        except AttributeError:
            desc = False
        if not desc:    
            try: desc = what.standard_name
            except AttributeError:
                desc = 'none found'
        print ('\t\tdescription: '+desc.replace('_',' '))
        print ('\t\tdims: '+str(what.dimensions))
        print ('\n')
        print ('\tPETURBED (%s)'%self.peturbedname)
        what = self.peturbed.variables[stashcode]
        try: desc = what.long_name
        except AttributeError:
            desc = False
        if not desc:    
            try: desc = what.standard_name
            except AttributeError:
                desc = 'none found'
        print ('\t\tdescription: '+desc.replace('_',' '))
        print ('\t\tdims: '+str(what.dimensions))
        
    def get_vars(self,stashcode:str):
        '''
        Retrieve the variables from each Dataset
        
        Arguments:     
           stashcode:str - the stashcode id
        Returns:
            dict: a dictionary containing the variable data with keys {base,perturbed}
        '''

        if stashcode not in self.varboth:
            print('Stashcode %s does not exist in both files')
            return None
        return {'base':self.base.variables[stashcode][:],
                'peturbed':self.peturbed.variables[stashcode][:]}
                
    def gettime(self, which='base'):
        ''' 
        Get the datetime for each value
        
        Arguments:
            'base' or 'peturbed'
            
        Returns:
            dict: {key:datetimestr, var:index}
        '''
        from datetime import datetime
        return dict([[datetime.fromtimestamp(i*60*60).strftime('%d-%m-%Y %M:%H'),i] for i in getattr(self,which).variables['time'][:]])
        
    
    def compareplot(self,stashcode:str,params,projection = ccrs.PlateCarree(),cmap = 'viridis',figsize=(20, 10),save = False):
        
        '''
            stashcode:str - what to plot
            params:dict - the same params are used for both (base peturbed)
            params:list[base,peturbed] - individual params are used [base, peturbed]

        '''
        
        if type(params) == dict:
            baseparams = peturbedparams = params
        elif type(params) == list:
            baseparams = params[0]
            peturbedparams = params[1]
    
        maintitle = '%s - base:%s peturbed:%s'%(stashcode,baseparams,peturbedparams)  
    
            
        ### dataset loads ##[]#
        lats = self.base.variables['latitude'][:]
        lons = self.base.variables['longitude'][:]
        assert (self.peturbed.variables['latitude'][:] == lats).all(), 'checking if the latitudes match'

        
        basedata = self.base.variables[stashcode]
        peturbeddata = self.peturbed.variables[stashcode]
        
        dims = self.dims(stashcode)
        for i in dims['base'][:-2]:
            basedata = basedata[baseparams[i]]
        for i in dims['peturbed'][:-2]:
            peturbeddata = peturbeddata[peturbedparams[i]]
            
        if basedata.shape != peturbeddata.shape:
            print('-- dimensions do not match, check you have supplied all dimensions --')
            print (basedata.shape , peturbeddata.shape)
            self.stashinfo(stashcode)
            return None
        
        

        #### Plot Fn ###

        fig = plt.figure(figsize=figsize)
        fig.suptitle(maintitle, fontsize=16)
        
        
        axes_class = (GeoAxes,dict(map_projection=projection))
        axgr = AxesGrid(fig, 111, axes_class=axes_class,
                        nrows_ncols=(3,2),
                        axes_pad=0.6,
                        cbar_location='bottom',
                        cbar_mode='each',
                        cbar_pad=0.5,
                        cbar_size='4%',
                        label_mode='')  # note the empty label_mode

        
        for i, ax in enumerate(axgr):
            ''' 
            Plot each timestep in a new cell
            '''
            ax.coastlines()
            ax.set_xticks(np.linspace(-180, 180, 5), crs=projection)
            ax.set_yticks(np.linspace(-90, 90, 5), crs=projection)
            
            lon_formatter = LongitudeFormatter(zero_direction_label=True)
            lat_formatter = LatitudeFormatter()
            ax.xaxis.set_major_formatter(lon_formatter)
            ax.yaxis.set_major_formatter(lat_formatter)
            
            if i==0: 
                data = basedata
                title = 'base:  '+self.basename
            if i==1: 
                data = peturbeddata
                title = 'peturbed:  '+self.peturbedname
            if i==2:
                data = basedata-peturbeddata
                title = 'base - peturbed'
            if i==3:
                data = peturbeddata - basedata
                title = 'peturbed - base '
            if i==4:
                data = basedata / peturbeddata
                title = 'base / peturbed'
            if i==5:
                data = peturbeddata / basedata
                title = 'peturbed / base '
            
            p = ax.contourf(lons, lats, data,
                            transform=projection,
                            cmap=cmap)
            
            axgr.cbar_axes[i].colorbar(p)
            
            ax.set_title(title)
        
            
            
        ### plot or save ### 
        
        plt.tight_layout()
        
        if save:
            fn = str(save).replace('.pdf','')+'.pdf'
            plt.savefig(fn)
            print('saved to :'+fn)
        else:
            plt.show()