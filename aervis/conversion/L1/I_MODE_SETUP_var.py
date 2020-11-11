"""

Routine to store model variables not given in the ouput files.

Variables are set within the modules file, depending on the I_MODE_SETUP used


"""

# import UKCA_lib as ukl
# reload(ukl)
# import matplotlib.pyplot as plt
# import iris

I_MODE_SETUP=8#is this the number for this setup? I set it to 8 as example
#we can add later on the I_MODE_SETUP to be read as an argument when you run the script

if I_MODE_SETUP==8:
    # Modal based paramters that are dependent on the I_MODE_SETUP of the model

    mode_names=["nucsol","aitsol","accsol","corsol","aitins","accins","corins"]

    # Mode switches (1=on, 0=0ff)
    mode_choice=[1,1,1,1,1,1,1]

    # Specify which modes are soluble
    # Mode names
    modesol=[1,1,1,1,0,0,0]

    # Mode width
    sigma=[1.59,1.59,1.40,2.0,1.59,1.59,2.0]

    # Specify size limits of geometric mean diameter for each mode (ddp - dry diameter of particle, m)
    # Lower Limit of Mode: ddplim0
    ddplim0=[1.0e-9,1.0e-8,1.0e-7,0.5e-6,1.0e-8,1.0e-7,1.0e-6]
    # Upper Limit of Mode: ddplim1
    ddplim1=[1.0e-8,1.0e-7,0.5e-6,1.0e-5,1.0e-7,1.0e-6,1.0e-5]


    # Species (Component) based paramters that are dependent on the I_MODE_SETUP of the model

    # Component names
    component_names= ["so4","bc","oc","ss","dust"]#,"sec_org"]#do we have secondary organics??
    kappa_component=[   0.61,    0.00,    0.10,    1.28,    0.00]#, 0.1]#check seconday organics I setted it to the same as organics but need to check. Jesus
    # Molar Mass kg / mol
    mm= [0.098,0.012,0.0168,0.05844,0.100]#,0.0168]

    # Density
    rhocomp=[1769.0,1500.0,1500.0,1600.0,2650.0]#,1500.0]#kg/m3
    
    
    
    
    

    
'''
ukca library

use this instead rhocomp[ims.component_names.index(comp_name)]


class SpeciesAttributes:
    def __init__(self,name,mm,rhocomp,kappa,description='None'):
        self.name=name
        self.mm=mm
        self.rhocomp=rhocomp
        self.kappa=kappa
        self.description=description


class ModalAttributes:
    def __init__(self,name,sigma,ddplim0,ddplim1,modesol,mode_choice,description='None'):
        self.name=name
        self.sigma=sigma
        self.ddplim0=ddplim0
        self.ddplim1=ddplim1
        self.modesol=modesol
        self.mode_choice=mode_choice
        self.description=description
        
        
'''

