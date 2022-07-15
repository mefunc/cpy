import os,glob
from threading import Thread
from Localdailypaper import *
from iniconfig import configok
dc=configok()
if dc[0]:
    dc[2].close()
    if dc[1]=='all':
        for pyfile in glob.glob('%s%sLocaldailypaper%s*.py'%(os.path.dirname(os.path.abspath(__file__)),os.sep,os.sep)):
            func=pyfile[pyfile.rfind(os.sep)+1:pyfile.rfind('.')]
            if '__' not in func:
                Thread(target=locals()[func].Upload).start()
    else:
        for func in dc[1].split(','):
            if '__' not in func:
                Thread(target=locals()[func].Upload).start()