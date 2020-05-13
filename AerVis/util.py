'''
A collection of functions useful for computation
'''

__all__='chunk'.split()

# def fchunk(L:list,by:int,fn=lambda x:x,kwargs:dict={}):
#     '''
#     A uniform chunk generator (unordered)
#     D.Ellis 
#     ''' 
#     # inc =  -(- (mx-1) // by) 
#     # '''// rounds down, so we take advantage of this using negatives to round up, but we need to adujst the max length this once''' 
#     for ix in range(by):
#         yield fn(L[ix::by],**kwargs)


def chunk(L:list,by:int):
    '''
    A uniform chunk generator (unordered)
    D.Ellis 
    ''' 
    # inc =  -(- (mx-1) // by) 
    # '''// rounds down, so we take advantage of this using negatives to round up, but we need to adujst the max length this once''' 
    for ix in range(by):
        yield L[ix::by]
                