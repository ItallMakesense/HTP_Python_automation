import subprocess as sp
import os
import sys

from constants import *
from tear_down import remove


RUN_DIR = os.path.dirname(__file__)
if not RUN_DIR:
    RUN_DIR = os.path.dirname(os.path.abspath(__file__))

def setup_venv():
    sp.run(['pip', 'install', 'virtualenv'])
    sp.run(['virtualenv', ENV_PATH])
    sp.run([PIP_PATH, 'install', 'fabric3'])

# 1
setup_venv()

# 2 - THERE WILL BE TEST RUNNER
if not CLIENT_HOST_PASSWORD:
    CLIENT_HOST_PASSWORD = input('Enter local user password: ')

# result = sp.run('sudo -S {run_with} {file}'.format(run_with=PYTHON_PATH,
#                 file=os.path.join(RUN_DIR, 'test.py')), shell=True,
#                 input=(CLIENT_HOST_PASSWORD+'\n').encode(),
#                 stdout=sp.PIPE, stderr=sp.PIPE)
# print("TEST RUN RESULT:", result)
# print("TEST IS DONE IN", RUN_DIR)

cmd = sp.Popen('sudo -S {run_with} {file}'.format(run_with=PYTHON_PATH,
                file=os.path.join(RUN_DIR, 'test.py')), shell=True,
                stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
result, errors = cmd.communicate(input=(CLIENT_HOST_PASSWORD+'\n').encode())
print("TEST RUN RESULT:", result.decode())
print("TEST RUN ERRORS:", errors.decode())
print("TEST IS DONE IN", RUN_DIR)

remove(ENV_PATH)
