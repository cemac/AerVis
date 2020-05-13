'''
The AerVis dataset class
This contains functions regarding all Levels of the library code. 
'''
import os,xarray

class AerData():
    '''
    The data class for model output. 
    
    
    '''

    
    def __init__(self,name:str, __FILES__:list=False,__LOC__:str=False):
        '''
        On initiation, the class checks for a netCDF file which exists with the provided 'name'. If such a file does not exist we run the L0 processing module and create one. 
        
        If such a file exists, it is loaded instead.  
        
        To append to an existing file, supply a list of __FILES__. This is compared to the existing .nc dataset, and any missing datapoints are appended using the "append_l0" function.
        
        '''
        
        if not __LOC__ : __LOC__ = os.getenv('AV_LOC',os.getcwd()+'/')
        
        self.name = name.strip('.nc')
        
        self.nc_loc = '%s%s.nc'%(__LOC__,name)
        if os.path.exists(self.nc_loc):
            print ('---- Loading File ---- : '+self.nc_loc)
            self.exists = True
            self.data = xarray.open_dataset(self.nc_loc) 

        else:
            from . import L0
            self.data = L0.run(name, loc=__LOC__, ncpu = 4, __FILES__ = __FILES__)
        
        # APPENDFN
        self.files = self.data.attrs['files']
        if hasattr(self, 'exists') and __FILES__:
            if type(__FILES__)==list:
                print('append_l0(__FILES__)')
            else:
                print('get files')
                L0.get_names(name,path=__LOC__)
        
        
        
        
        
        
        
        self.classdescription = '''
        AerVis DataSet Class
        --------------------------------

        On initiation, the class checks for a netCDF file which exists with the provided 'name'. If such a file does not exist we run the L0 processing module and create one. 
        
        If such a file exists, it is loaded instead.  
        
        To append to an existing file, supply a list of __FILES__. This is compared to the existing .nc dataset, and any missing datapoints are appended using the "append_l0" function.
        
        
        Methods:
            - print(<this>) - gives the outline of the dataset structure.
            - split_var([variables]) - creates separate nc files for each defined variable 
            
            
       '''
        
    def keys(self):
        return dir(self)
        
    def __repr__(self):
         return self.classdescription
    def __str__(self):
         return  '''
         AerVis Variable Attributes Class
         --------------------------------
         ''' + self.data.__str__()
        