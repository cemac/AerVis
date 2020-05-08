import os

pwd = __file__.strip('makedoc.py')

code = pwd+'AerVis'
doc  = pwd+'Documentation'

cmd = 'pdoc --html %(code)s --output-dir %(doc)s --force'%{'code':code, 'doc':doc}
os.system(cmd)

print(cmd)
