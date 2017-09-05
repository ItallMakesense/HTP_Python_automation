# import subprocess as sp
# from constants import *


# passwd = input('Enter local user password:')
# result = sp.run(f"sudo -S {PYTHON_PATH} check.py", input=passwd.encode(), shell=True)
# print(result.stdout)
import os.path


print(__file__)
print(os.path.abspath(__file__))