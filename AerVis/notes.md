
### Variable dictionary
- variable dictionary changed to VariableReference class (var_ref), this allows the combination of stash codes and names as indexes pointing towards the same item. Unlike a multi-key dictionary, the use of a class (although having a larger overhead) means that if we edit part of the linked attribute, it is automatically updated for both keys (stash and name).
- file reading parsed by regex and added to numpy array, this allows vectorisation and a reduction of external conditional and loops
- zfill used over iterative conditionals for stash keys 