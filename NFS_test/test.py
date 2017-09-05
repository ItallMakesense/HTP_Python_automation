"""  """
import stat

from constants import *
import bridge
import set_up
import tear_down


# Test Set Up
def setup():
    # set up server
    remote_result = bridge.remote_shell('python3', SERVER_TEST_DIR, set_up, NFS_SERVER)
    print("SETUP REMOTE RESULT:", remote_result)
    print("REMOTE WORK IS DONE")

    # set up client
    set_up.client()
    return remote_result

# TEST

# Test Set Up
def teardown():
    # tear down client
    tear_down.client()
    print("LOCAl WORK IS DONE")
    # tear down server
    remote_result = bridge.remote_shell('python3', SERVER_TEST_DIR, tear_down, NFS_SERVER)
    return remote_result

print(setup())
print("="*80)
print(teardown())

# TRY TO PUT SEVERAL FILES THROUGH FABRIC
