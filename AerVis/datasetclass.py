'''
The AerVis dataset class
This contains functions regarding all Levels of the library code. 
'''
import os,xarray,time,re

''' file arguments''' 
engine = 'netcdf4'
lock = None
coompute=False


class AerData():
    '''
    The data class for model output. 
    
    
    '''

    
    def __init__(self,name:str, __FILES__:list=False,__LOC__:str=False):
        '''
        On initiation, the class checks for a netCDF file which exists with the provided 'name'. If such a file does not exist we run the L0 processing module and create one. 
        
        If such a file exists, it is loaded instead.  
        
        To append to an existing file, supply a list of __FILES__. This is compared to the existing .nc dataset, and any missing datapoints are appended using the "append_l0" function.
        
        Arguments:
            __FILES__ - files to concat 
            __LOC__   - location to save files
            
            
        Updatable load profiling (time taken to .compute() dask dataset into memory ): 
        
            In [2]: d = AerData('bk417a',lazy=False)                                    
            ---- Loading File ---- : /Users/wolfiex/UKCA_postproc/data/bk417a.nc
             30.91 loadtime - lazy: False

            In [3]: d = AerData('bk417a',lazy=True)                                   
            ---- Loading File ---- : /Users/wolfiex/UKCA_postproc/data/bk417a.nc
             0.05 loadtime - lazy: True


        '''
        
        if not __LOC__ : __LOC__ = os.getenv('AV_LOC',os.getcwd()+'/')
        
        self.name = name.strip('.nc')
        
        self.model = 'UKCA'
        
        self.nc_loc = '%s%s.nc'%(__LOC__,name)
        
        if os.path.exists(self.nc_loc):
            print ('---- Loading File ---- : '+self.nc_loc)
            self.exists = True
            start = time.perf_counter()
            self.data = xarray.open_dataset(self.nc_loc, engine=engine,lock=lock)
            print (' %.2f s loadtimeself'%(time.perf_counter() - start) )
                        
        else:
            from . import L0
            self.data = L0.run(name, loc=__LOC__, ncpu = 4, __FILES__ = __FILES__)
            # As this does not exist, create it 
            print('saving - this is the slow bit')
            
            start = time.perf_counter()
            self.data.compute()
            self.data.to_netcdf(path=self.nc_loc, mode='w', format='NETCDF4',compute=compute)         
            end = time.perf_counter() - start
            print (' %.2f minutes - written to %s'%(end/60,self.nc_loc) )
            
            ## L1 append coords
            from .L1.coords import coord_list
            self.add_coords(coord_list)
            print('coords loaded, but not added to netCDF file')
             
        
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
            
        KeyAttrs:
            .data - provides the open netCDF dataset
            
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
         
         
    def add_coords(self,coordinates:list):
        '''
        A function to append additional coordinates to the DataSet
        coord_list: nested *list* with  (value, standard_name, long_name, units) for each item
        '''
        from .L1 import coords 
        self.data = coords.add(self.data,coordinates)
        
    def get_coords(self):
        ''' returns the dataset coordinates '''
        return self.data.coords
        
    def get_attrs(self):
        ''' returns the dataset attributes '''
        return self.data.attrs
        
        
    def update(self,attrs:dict=False,datasets:dict=False,coords:xarray.core.coordinates.DatasetCoordinates=False,err=False):
        '''
        A function to append information to the dataset file. 
        
        WARNING! existing variables are replaced with the new values

        Inputs:
            attrs - a dictionary containing all attributes to append 
            datasets - a dictionary containing all datasets to appended
            coordinates - an xarray coordinate dataset
            
            
        note cannot overwrite coordinates?
    
        '''
        import time
        new = xarray.Dataset()
        
        if attrs:
            assert type(attrs) is dict, 'Attributes not dictionary'
            new.attrs=attrs
        if coords:
            assert type(coords) is xarray.core.coordinates.DatasetCoordinates , 'Coordinates not in format: '+type(xarray.core.coordinates.DatasetCoordinates)       
            new.coords = coords 
        if datasets:
            assert type(dataset) is dict, 'Dataset not a dictionary'
            
            for var in dataset:
                new[var] = dataset[var]
                
        print('-- Updating %s --'%self.nc_loc) 
        # close dataset 
        self.data.close()
        
        # append new dataset to existing file
        start = time.perf_counter()
        try:new.to_netcdf(self.nc_loc,mode='a',format='NETCDF4')
        except OSError as e:
            if err:
                import sys 
                sys.exit(e)
                
            print('''
            --- Failed at update ---
             This is likely because the file is already open in another process. 
             Closing all files which have the file open using:
                lsof %s (finds all processes which have the file open)
                kill -9 pid (kills each process id from lsof)
            --- Trying again ---
             '''%self.nc_loc)
            
            pids= [None]*2
            while len(pids)>0:
                print('Waiting for open instances to end...')
                proc = os.popen('lsof %s'%self.nc_loc).read()
                pids = re.findall(r'\n[^\s]* (\d+)',proc) 
                for i in pids: os.popen('kill -9 %d'%int(i)).read()
                time.sleep(2)# wait for the processe to end 
             
            self.update(attrs=attrs,datasets=datasets,coords=coords,err=True)
             
              
            
        end = time.perf_counter() - start
        print (' %.2f minutes - appended to %s'%(end/60,self.nc_loc) )
        # reopen dataset
        self.data = xarray.open_dataset(self.nc_loc, engine=engine,lock=lock)


'''xarray.open_mfdataset
xarray.open_mfdataset(paths, chunks=None, concat_dim='_not_supplied', compat='no_conflicts', preprocess=None, engine=None, lock=None, data_vars='all', coords='different', combine='_old_auto', autoclose=None, parallel=False, join='outer', attrs_file=None, **kwargs)
Open multiple files as a single dataset.'''        
        
