from netCDF4 import Dataset as netcdf_dataset
from . import single

class AerData():
    '''
    The plotting Class
    '''

    
    def __init__(self,filename:str):
        '''
        Arguments:
            filename - the full path to the netCDF file we wish to load
        '''
        self.data = netcdf_dataset(filename)
        
        self.vars = self.data.variables
            
            
    def show_var(self, screen:bool=True,returnstr:bool=False):
        '''
        
        Show variables within the Dataset
        If available this includes the standard/long name and dims
        
        Arguments:
            screen: bool - print to screen
            returnstr: bool - returns the string for saving to a file.. 
        '''
        rtstr=''
        for i in self.data.variables:
            dt = self.data[i]
            try: longname = dt.long_name
            except AttributeError: 
                try: longname = ' '.join(dt.standard_name.split('_')).title()
                except: longname = ''
            
            rtstr+='%11s - %s - %s\n'%(i,self.data[i].dimensions,longname)
            
        if screen: print(rtstr)
        
        if returnstr: return rtstr
        
    def get_times(self,datetimedict=False):
        '''
        Return the times of each dataset timesteps
        
        Arguments:
            datetimedict:bool - return a datetime (key, value) dictionary
        '''
        if datetimedict:
            from datetime import datetime
            return dict([[datetime.fromtimestamp(i*60*60).strftime('%D'),i] for i in self.data.variables['time']])
        else:   return list(self.data.variables['time'])
        
    def get_var(self,variable:str):
        '''
        Return a variable from the Dataset
        '''
        return self.data[variable]
        
    def singleplot(self,what,**kwargs):
        '''
        A wrapper function for aervis.plotting.single.singleplot
        
        Arguments:
            what:str - The stash key variable name
        
        optional arguments:  
            level:int - the required level when dealing with pseudo or model_level
            t_steps:list - a list of selected timesteps in the same format as self.data.variables['time']
            figsize:tuple - figure size in inches
            col:int - number of columns in plot grid
            save:str - file name with path of where to save the figure. Enabling this does not show the figure on screen. 
                  
            projection; - cartopy projection
            cmap:str - colourmap name
            vmin:float - manual min colourmap value
            vmax:float - manual max colourmap value
            discrete_cbar:bool - continuous or discrete colourbar values
        '''
        
        single.singleplot(self.data,what,**kwargs)
