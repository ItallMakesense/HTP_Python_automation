""" Description """
import subprocess as sp

from config import CLIENT_HOST_PASSWORD, SERVER_HOST_PASSWORD,\
                   ENV_PATH, PIP_PATH, PYTHON_PATH, LOG_NAME
from tear_down import remove_dir
import common

# TO DO !!!
class BaseTest:
    """ Description """

    def setup_method(self, method):
        """ Description """
        # set up server
        LOG.info(common.MAKE_CAP("Server setup"))
        bridge.prepare(LOG, SERVER_TEST_DIR)
        bridge.remote_shell(LOG, 'python3', SERVER_TEST_DIR, set_up, NFS_SERVER,
                            ','.join(EXPORTS_OPTIONS))
        # set up client
        LOG.info(common.MAKE_CAP("Client setup"))
        set_up.client(LOG)

    # Test Tear Down
    def teardown_method(self, method):
        """ Description """
        # tear down client
        LOG.info(common.MAKE_CAP("Client teardown"))
        tear_down.client(LOG)
        # tear down server
        LOG.info(common.MAKE_CAP("Server teardown"))
        bridge.remote_shell(LOG, 'python3', SERVER_TEST_DIR, tear_down, NFS_SERVER,
                            ','.join(EXPORTS_OPTIONS))


def setup_venv():
    """ Description """
    setup_order = [
        ['pip', 'install', 'virtualenv'],
        ['virtualenv', ENV_PATH],
        [PIP_PATH, 'install', 'fabric3', 'pytest']
        ]
    for step in setup_order:
        result = common.execute(step, stdout=sp.PIPE, stderr=sp.PIPE)
        common.write_to({LOG.debug: result[0].decode(), LOG.error: result[1].decode()})

# Logger initialising
RUN_DIR, LOG, LOG_FILE = common.initiate_logger(LOG_NAME, __file__)

# finding password
if not CLIENT_HOST_PASSWORD:
    CLIENT_HOST_PASSWORD = input('Enter local host password: ')
if not SERVER_HOST_PASSWORD:
    SERVER_HOST_PASSWORD = input('Enter remote host password: ')

# virtualenv installation
LOG.info(common.MAKE_CAP("Environment installation"))
setup_venv()

# test execution in a subprocess
LOG.info(common.MAKE_CAP("Testing start"))
result = common.execute(['sudo', '-S', PYTHON_PATH, '-m', 'pytest', '-s', RUN_DIR],
                        stdin=sp.PIPE, stderr=sp.PIPE, stdout=sp.PIPE,
                        input_line=CLIENT_HOST_PASSWORD)
common.write_to({LOG.debug: result[0].decode(), LOG.error: result[1].decode()})
LOG.info(common.MAKE_CAP("Testing end"))

# removing virtualenv
LOG.info(common.MAKE_CAP("Environment removing"))
try:
    remove_dir(ENV_PATH)
except OSError as error:
    common.write_to({LOG.error: error})
else:
    common.write_to({LOG.debug: ' '.join(("Removed -", ENV_PATH))})
