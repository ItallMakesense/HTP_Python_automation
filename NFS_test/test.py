""" Description """
import logging

from config import *
import bridge
import set_up
import tear_down


# Test Set Up
def setup():
    """ Description """
    # set up server
    bridge.remote_shell('python3', SERVER_TEST_DIR, set_up, NFS_SERVER)
    #
    print("REMOTE WORK IS DONE")
    # set up client
    set_up.client()

# TEST

# Test Set Up
def teardown():
    """ Description """
    # tear down client
    tear_down.client()
    #
    print("LOCAl WORK IS DONE")
    # tear down server
    bridge.remote_shell('python3', SERVER_TEST_DIR, tear_down, NFS_SERVER)

# 1
setup()

# 2
teardown()
