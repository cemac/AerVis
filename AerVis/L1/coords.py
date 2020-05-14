''' 
A file containing all the coordinates which need to be added to a DataSet

coord_list: nested *list* with  (value, standard_name, long_name, units) for each item


'''

__all__= 'coord_list add'.split()

coord_list = [
# (1000.0,'p0','reference_pressure','hPa')
# (100000.0,'p_convert','convert_units','Pa')
(287.058,'r_specific','R_specific','J-kilogram^-1-kelvin^-1'),#J/(kg·K)
  
(28.991e-3,'molar_mass_air','Molar mass of air','kilogram-mole^-1'),#J/(kg·K)
(6.022e23,'avogadro','Avogadros number - particles per mol','mole^-1'),#J/(kg·K)

]


def add(dataset ,coords:list=coord_list):
    ''' A function to add / update coordinates of a dataset '''
    
    for c in coords:
        dataset.coords[c[1]]=c[0]
        dataset.coords[c[1]].attrs = {'standard_name':c[2],'units':c[3]}
        
    return dataset
    
    
    