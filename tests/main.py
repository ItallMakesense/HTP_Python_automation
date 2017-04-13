import pip
import unittest
import platform
import os
import sys
import time

if platform.system() != 'Linux':
    sys.exit('Your system is not Linux. Test aborted.')

def package_needed(package):
    for i in pip.get_installed_distributions():
        if package in str(i):
            return False
    
if package_needed("paramiko"):
    can = subprocess.PIPE
    proc = subprocess.Popen("sudo -S pip install paramiko", shell=True, stdin=can, stdout=can, stderr=can)
    outs, errors = proc.communicate(input="{}\n".format(server_password).encode())
if not package_needed("paramiko"):
    import paramiko
    import enviro

@enviro.client_connect
def executor(command, ssh='connect'):
    stdin, stdout, stderr = ssh.exec_command("sudo -S {}".format(command))
    stdin.write("{}\n".format(enviro.client_password).encode())
    stdin.flush()
    return stderr.read().decode()

class MainTest(unittest.TestCase):

    def setUp(self):
        self.env_log = os.getcwd()+'/enviro.log'

        open(self.env_log, 'w').close()
        with open(self.env_log, "a") as log:
            enviro.server_nfs(enviro.nfs_setup_commands, log)
            log.write('\n')
            enviro.client_nfs(enviro.nfs_remote_commands, log)

        testNames = ['roTest', 'rwTest', 'ownTest']

        self.suite = unittest.TestSuite()
        loader = unittest.defaultTestLoader
        for test in testNames:
            testCase = loader.loadTestsFromModule(__import__(test))
            self.suite.addTest(testCase)

    def test_all_tests(self):
        tests_log = os.getcwd()+'/tests.log'
        open(tests_log, 'w').close()
        with open(tests_log, "a") as log:
            log.write(time.ctime()+'\n')
            unittest.TextTestRunner(stream=log, verbosity=2).run(self.suite)

    def tearDown(self):
        with open(self.env_log, "a") as log:
            log.write('\n')
            enviro.client_nfs(enviro.end_remote_commands, log)
            log.write('\n')
            enviro.server_nfs(enviro.end_nfs_commands, log)

if __name__ == "__main__":
    unittest.main(verbosity=2)




