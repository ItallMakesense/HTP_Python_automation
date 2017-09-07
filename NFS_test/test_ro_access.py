""" Description """
import pytest
import os

from config import SERVER_TEST_DIR, CLIENT_TEST_DIR, GET_TEST_PATH, NFS_SERVER
import common
import bridge
import set_up
import tear_down


RUN_DIR, LOG, LOG_FILE = common.initiate_logger(__name__, __file__)
TEST_FILE_PATH = GET_TEST_PATH(CLIENT_TEST_DIR)

EXPORTS_OPTIONS = ['ro', 'sync', 'no_subtree_check']

# Test Set Up
def setup_function(function):
    """ Description """
    # set up server
    LOG.info(common.MAKE_CAP("Server setup"))
    bridge.prepare(LOG, SERVER_TEST_DIR)
    bridge.remote_shell(LOG, 'python3', SERVER_TEST_DIR, set_up, NFS_SERVER,
                        ','.join(EXPORTS_OPTIONS))
    # set up client
    LOG.info(common.MAKE_CAP("Client setup"))
    set_up.client(LOG)

def test_creation(capsys):
    """ Description """
    new_file_path = os.path.join(CLIENT_TEST_DIR, 'test_creation')
    LOG.info(common.MAKE_CAP("Creation test start"))
    try:
        with open(new_file_path, 'w') as file:
            LOG.info("Successfully created -", new_file_path)
            LOG.info("Test passed")
    out, err = capsys.readouterr()
    common.write_to({LOG.debug: out, LOG.error: err})
    LOG.info(common.MAKE_CAP("Creation test end"))

def test_edition(capsys):
    """ Description """
    LOG.info(common.MAKE_CAP("Edition test start"))
    with open(TEST_FILE_PATH, 'w') as file:
        file.write("Test succeeded")
        print("Successfully edited -", TEST_FILE_PATH)
    out, err = capsys.readouterr()
    common.write_to({LOG.debug: out, LOG.error: err})
    LOG.info(common.MAKE_CAP("Edition test end"))

def test_deletion(capsys):
    """ Description """
    LOG.info(common.MAKE_CAP("Deletion test start"))
    os.remove(TEST_FILE_PATH)
    if not os.path.exists(TEST_FILE_PATH):
        print("Successfully deleted -", TEST_FILE_PATH)
    out, err = capsys.readouterr()
    common.write_to({LOG.debug: out, LOG.error: err})
    LOG.info(common.MAKE_CAP("Deletion test start"))

# Test Tear Down
def teardown_function(function):
    """ Description """
    # tear down client
    LOG.info(common.MAKE_CAP("Client teardown"))
    tear_down.client(LOG)
    # tear down server
    LOG.info(common.MAKE_CAP("Server teardown"))
    bridge.remote_shell(LOG, 'python3', SERVER_TEST_DIR, tear_down, NFS_SERVER,
                        ','.join(EXPORTS_OPTIONS))
