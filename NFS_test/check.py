from subprocess import check_output


print(check_output('which pip', shell=True).decode().strip())
