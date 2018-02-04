import os

basedir = os.path.abspath(os.path.dirname(__file__))    #/home/pi/Production/teleinfo/teleinfoapp/
print basedir
pdir = os.path.dirname(basedir)                         #/home/pi/Production/teleinfo/
print pdir
parentdir = os.path.dirname(pdir)                    #/home/pi/Production/
print parentdir
parentdirname = os.path.basename(parentdir)             #Production/
print parentdirname
