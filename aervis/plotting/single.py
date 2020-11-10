'''
A series of plotting functions for a single file




'''
#imports
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colorbar,colors,rcParams
rcParams['mpl_toolkits.legacy_colorbar'] = False
from datetime import datetime
import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from mpl_toolkits.axes_grid1 import AxesGrid
import numpy as np


def singleplot(dataset,what:str,t_steps=False,projection = ccrs.PlateCarree(),cmap = 'twilight',vmin = False,vmax = False,discrete_cbar = True,level=0,figsize=(20, 10),col:int = 2,save = False,tname='time'):
    
    '''
    Single n*2 plot grid of the dataset spanning timestep
        Arguments:
            what:str - The stash key variable name
        
        optional arguments:  
            level:int - the required level when dealing with pseudo or model_level
            t_steps:list - a list of selected timesteps in the same format as self.data.variables['time']
            figsize:tuple - figure size in inches
            save:str - file name with path of where to save the figure. Enabling this does not show the figure on screen. 
            col:int - number of columns
                  
            projection; - cartopy projection
            cmap:str - colourmap name
            vmin:float - manual min colourmap value
            vmax:float - manual max colourmap value
            discrete_cbar:bool - continuous or discrete colourbar values
            tname:str - time variable name - do not change
    '''
    
    
    ### dataset loads ###
    lats = dataset.variables['latitude'][:]
    lons = dataset.variables['longitude'][:]
    data = dataset.variables[what]
    times = dataset.variables[tname][:]
    dims = data.dimensions
    ##### Pre-plot datamangling #####
    
    try: name = ' '.join(data.long_name.split('_')).title()
    except AttributeError: 
        try: name = ' '.join(data.standard_name.split('_')).title()
        except AttributeError: name = what

    
    if len(data.shape) > 2 and tname=='time':
        '''
        Additional dimensions are fustrating as there is no pattern to where they appear
        
        (time, model_level_number, latitude, longitude)
        (pseudo_level,time, latitude, longitude)
        '''
        
        dlevel = list(filter(lambda x: x not in 'time latitude longitude'.split(),dims))[0]
        print(dlevel,dims)
        print( '''\n    --- ONLY DISPLAYING A SINGLE %s --- \n 
        The level currently selected is %d, To change this use the pseudolevel argument. '''%(dlevel,level) )
        ix = dims.index(dlevel)
        if ix ==0: data = data[level]
        elif ix ==1:data = data[:,level]
        elif ix ==2:data = data[:,:,level]
        elif ix ==3:data = data[:,:,:,level]
    else:
        ix = dims.index('time')
        if ix ==0: data = data[level]
        elif ix ==1:data = data[:,level]
        elif ix ==2:data = data[:,:,level]
        elif ix ==3:data = data[:,:,:,level]
        


    hastime = True
    if 'time' not in dims and tname == 'time':
        nval = 1
        hastime=False
    elif not t_steps:
        nval = data.shape[0]
    else:
        select = [i in t_steps[:] for i in times]
        nval = sum(select)
        assert nval > 0, 'no time matches between arrays'
        data = data[select]
        times = times[select]
        
    if not vmin: vmin = data.min()
    if not vmax: vmax = data.max()
    if tname =='time':
        times = [datetime.fromtimestamp(i*60*60).strftime('%d-%m-%Y %M:%H') for i in times]
        


    #### Plot Fn ###


    fig = plt.figure(figsize=figsize)
    fig.suptitle(name, fontsize=16)
    
    if nval == 1: col = 1
    rows = int(np.ceil(nval/col))
    
    axes_class = (GeoAxes,dict(map_projection=projection))
    axgr = AxesGrid(fig, 111, axes_class=axes_class,
                    nrows_ncols=(rows,col),
                    axes_pad=0.6,
                    cbar_location='right',
                    cbar_mode='single',
                    cbar_pad=0.2,
                    cbar_size='3%',
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
        
        
        if i >= len(times):
            ax.cla()
            ax.axis("off")
        elif hastime:
            p = ax.contourf(lons, lats, data[i, ...],
                            transform=projection,
                            cmap=cmap,vmin=vmin, vmax=vmax)
            ax.set_title(times[i])
        else:# variable is not time dependant
            p = ax.contourf(lons, lats, data[:,:],
                            transform=projection,
                            cmap=cmap,vmin=vmin, vmax=vmax)

    ### Colourmap setup ####

    cmap = getattr(mpl.cm,cmap)

    if discrete_cbar:
        bounds = [float('%.01e'%i) for i in np.linspace(vmin,vmax,9)]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
    else:
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

    cb = mpl.colorbar.ColorbarBase(axgr.cbar_axes[0], cmap=cmap,norm=norm,orientation='vertical')
        
    
    ### plot or save ### 
    
    plt.tight_layout()
    
    if save:
        fn = str(save).replace('.pdf','')+'.pdf'
        plt.savefig(fn)
        print('saved to :'+fn)
    else:
        plt.show()
