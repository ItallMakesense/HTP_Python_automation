""" Description """
import pytest
import time

from config import SERVER_TEST_DIR, NFS_SERVER
import common
import bridge
import set_up
import tear_down


RUN_DIR, LOG, LOG_FILE = common.initiate_logger(__file__)

EXPORTS_OPTIONS = ['rw', 'sync', 'no_root_squash']

# Test Set Up
def setup_module(module):
    """ Description """
    # set up server
    LOG.info("SERVER SETUP".center(80, '='))
    bridge.prepare(SERVER_TEST_DIR)
    bridge.remote_shell('python3', SERVER_TEST_DIR, set_up, NFS_SERVER,
                        ','.join(EXPORTS_OPTIONS))
    # set up client
    LOG.info("CLIENT SETUP".center(80, '='))
    set_up.client()

def test(capsys):
    """ Description """
    LOG.info("TEST BEGUN".center(80, '='))
    print("IT WORKED")
    time.sleep(5)
    out, err = capsys.readouterr()
    common.write_to({LOG.debug: out, LOG.error: err})
    LOG.info("TEST ENDED".center(80, '='))

# Test Tear Down
def teardown_module(module):
    """ Description """
    # tear down client
    LOG.info("CLIENT TEARDOWN".center(80, '='))
    tear_down.client()
    # tear down server
    LOG.info("SERVER TEARDOWN".center(80, '='))
    bridge.remote_shell('python3', SERVER_TEST_DIR, tear_down, NFS_SERVER,
                        ','.join(EXPORTS_OPTIONS))
