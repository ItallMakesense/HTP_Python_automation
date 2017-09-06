""" Description """
import subprocess as sp

from config import CLIENT_HOST_PASSWORD, SERVER_HOST_PASSWORD,\
                   ENV_PATH, PIP_PATH, PYTHON_PATH
from tear_down import remove_dir
import common


def setup_venv():
    """ Description """
    setup_order = [
        ['pip', 'install', 'virtualenv'],
        ['virtualenv', ENV_PATH],
        [PIP_PATH, 'install', 'fabric3', 'pytest']
        ]
    for step in setup_order:
        result = common.execute(step, stdout=sp.PIPE, stderr=sp.PIPE)
        common.write_to({LOG.debug: result[0].decode(),
                        LOG.error: result[1].decode()})

# Logger initialising
RUN_DIR, LOG, LOG_FILE = common.initiate_logger(__file__)

# finding password
if not CLIENT_HOST_PASSWORD:
    CLIENT_HOST_PASSWORD = input('Enter local host password: ')
if not SERVER_HOST_PASSWORD:
    SERVER_HOST_PASSWORD = input('Enter remote host password: ')

# virtualenv installation
LOG.info("ENVIRONMENT INSTALLATION".center(80, '='))
setup_venv()

LOG_FILE.close()

# test execution in a subprocess
result = common.execute(['sudo', '-S', PYTHON_PATH, '-m', 'pytest', '-s', RUN_DIR],
                        stdin=sp.PIPE, input_line=CLIENT_HOST_PASSWORD)

# removing virtualenv
LOG.info("ENVIRONMENT REMOVING".center(80, '='))
try:
    remove_dir(ENV_PATH)
except OSError as error:
    common.write_to({LOG.error: error})
else:
    common.write_to({LOG.debug: ' '.join(("REMOVED -", ENV_PATH))})
