'''
The Variable Dictionary class
This contains all code for reading and updating the variable dictionary

Usage:

'''

import dill

class Attributes:
    '''An Attributes class'''
    def __init__(self, **entries):
        self.__dict__.update(entries)

class VariableReference(dict):
    '''
    A variable class mapping data two keys acting as pointers to the data. The keys are stash_name and stash_code - written as name and code. When data is updated on either variable, it updates for both
    
    Inputs:
        as_class :: bool- convert var dictionarys to allow for . access using the attributes class (dictionaries are faster)
    
    Usage:
        vars = VariableReference()
        vars.add(<key1>,<key2>,<data dictionary>)
    '''
    # bikey dictionary - updates data independantly
    # myDict = {
    #   **dict.fromkeys(['a', 'b', 'c'], 10), 
    #   **dict.fromkeys(['b', 'e'], 20)
    # }
    
    def __init__(self,as_class=False):
        self.as_class = as_class
        self.index = 0
        
        self.classdescription = '''
        AerVis Variable Attributes Class
        --------------------------------
        
        
        Methods:
           -   To get attributes run <this>.keys()
           -   To access articles with invalid python names (e.g. begining with \% or -) use getattr(<this>,"$£%$_unconventional_var_name")
       '''
        
    def keys(self):
        return dir(self)
    def __repr__(self):
         return self.classdescription
    def __str__(self):
         return  '''
         AerVis Variable Attributes Class
         --------------------------------
         Number of entries: %d
         '''%self.index
        
        
    def add(self,data):
        '''Add additional Data'''
        assert type(data) == dict
        
        # Add Mandatory keys as blanks
        for n in 'stash_code,name,short_name,long_name,units,description'.split(','):
            try:data[n]
            except KeyError: data[n] = ''
        
        name = data['name']
        code = data['stash_code']
        
        if self.as_class:
            data = Attributes(data)
        self.index+=1
        setattr(self, 'var_id_%i'%self.index, data)
        setattr(self, name ,getattr(self,  'var_id_%i'%self.index))
        setattr(self, code ,getattr(self,  'var_id_%i'%self.index))
        
        
    def match(self,snippet:str):
        ''' 
        Retrun all keys which contain the `snippet` string 
        
        if snippet == list, match all snippets
        '''
        if type(snippet) is str:
            return list(filter(lambda x: snippet.upper() in x, self.keys())) 
        else :
            keys = self.keys()
            for i in snippet:
                keys = list(filter(lambda x: i.upper() in x, keys) )
            return keys
                
                
                  
        
        
    def get(self, key):
        ''' Get value from using key. This is a wrapper for getattr'''
        
        return getattr(self,key)  
        
        
    def save(self,filename = False):
        '''
        A function to save the variable difference class 
        
        example usage:
            var_ref.save('<usefulidentifier>.dl')
        '''
        assert type(filename) is str
        dill.dump(self,open(filename,'wb'))
        print('Variable Dictionary Saved as ',filename)
        
    def load(self,filename = False):
        '''
        A function to populate the variable difference class using a saved version
        
        example usage:
            var_ref.load('<usefulidentifier>.dl')
            
            or 
            
            import dill 
            dill.load(open(<filename.dl>,'rb'))  
        '''
        assert type(filename) is str
        
        self = dill.load(open(filename,'rb'))        
        print('reloaded class information from ',filename)
        return self
        
    # def fromVarName(self,varstr):
    #     self.add(dict(( (i,globals()[i]) for i in varstr.split(','))) )

