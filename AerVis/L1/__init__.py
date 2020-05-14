'''
The L1 section of the AerVis code

This section gathers information about the simulation runs
'''



def run(self):
    
    
    # TEMPERATURE
    
    ''' 
    If data does not contain "temperature"
    '''
    
    if self.model == 'tomcat':
        self.temperature = self.data['m01s16i004'][0] ## temp
    else: 
        pT = self.data['m01s00i004'][0] ## potential temp
        
        
        
        # AIR Pressure only needed if temperature missing
    

    try:
        self.air_pressure=self.data['m01s00i408'][0]
        if self.air_pressure.shape != self.temperature.shape:
                    raise NameError('air pressure with different shape as potential_temperature')

    except NameError:
        ''' this will fall over''' 
        
        # manually  
        # air_pressure_nodim = self.data['m01s00i255'][0]
        # p_convert = iris.coords.AuxCoord(100000.0,
        #                           long_name='convert_units',
        #                           units='Pa')
        
        self.air_pressure=self.data['m01s00i255'][0]*100000.0


    # print 'potential temperature and air_pressure loaded'
    # p0 = iris.coords.AuxCoord(1000.0,
    #                               long_name='reference_pressure',
    #                               units='hPa')
    # p0.convert_units(air_pressure.units)

    '''
    p0= 100000 # 1 hPa = 100 Pa 
    Rd=287.05 # J/kg/K
    cp=1005.46 # J/kg/K
    '''
    if self.model != 'tomcat':
        self.temperature=pT*(air_pressure/100000.0)**(287.05/1005.46)
        
        
        
        
    '''
    filter nbr 
    filter mmr
    '''