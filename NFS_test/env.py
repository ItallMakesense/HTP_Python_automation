import subprocess as sp

from constants import *


sp.run(['pip', 'install', 'virtualenv'])
sp.run(['virtualenv', ENV_PATH])
sp.run([PIP_PATH, 'install', 'fabric3'])
